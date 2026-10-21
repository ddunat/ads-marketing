"""Reddit outreach for DC Building Inspectors.

Two commands:

  python reddit/bot.py find   Scan subreddits for threads about building
                              inspections, have Claude draft helpful replies,
                              and save each draft to reddit/queue/ as "pending".
  python reddit/bot.py post   Post every draft whose status is "approved",
                              within the limits in config.yaml.

A draft is never posted until a person changes its status to "approved".
"""

from __future__ import annotations

import json
import re
import sys
import time
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from pathlib import Path

import yaml
from pydantic import BaseModel

HERE = Path(__file__).resolve().parent
QUEUE = HERE / "queue"
STATE_FILE = HERE / "state.json"
LINK_RE = re.compile(r"https?://|dcinspect\.com", re.I)


# ---------- config, state, queue files ----------

def load_config() -> dict:
    return yaml.safe_load((HERE / "config.yaml").read_text())


def load_state() -> dict:
    if STATE_FILE.exists():
        return json.loads(STATE_FILE.read_text())
    return {"seen": [], "posted": []}


def save_state(state: dict) -> None:
    state["seen"] = state["seen"][-5000:]
    STATE_FILE.write_text(json.dumps(state, indent=2) + "\n")


@dataclass
class Draft:
    path: Path
    meta: dict
    body: str

    @classmethod
    def read(cls, path: Path) -> "Draft":
        text = path.read_text()
        _, header, body = text.split("---\n", 2)
        return cls(path, yaml.safe_load(header), body.strip())

    def write(self) -> None:
        header = yaml.safe_dump(self.meta, sort_keys=False, allow_unicode=True)
        self.path.write_text(f"---\n{header}---\n{self.body.strip()}\n")


def all_drafts() -> list[Draft]:
    return [Draft.read(p) for p in sorted(QUEUE.glob("*.md"))]


# ---------- Reddit ----------

def reddit_client():
    import os
    import praw

    return praw.Reddit(
        client_id=os.environ["REDDIT_CLIENT_ID"],
        client_secret=os.environ["REDDIT_CLIENT_SECRET"],
        username=os.environ["REDDIT_USERNAME"],
        password=os.environ["REDDIT_PASSWORD"],
        user_agent=f"python:dcinspect-reddit:v1.0 (by /u/{os.environ['REDDIT_USERNAME']})",
    )


def matches_keywords(text: str, keywords: list[str]) -> bool:
    text = text.lower()
    return any(k.lower() in text for k in keywords)


def candidate_threads(reddit, cfg: dict, state: dict, now: datetime) -> list:
    """New threads that mention a keyword, are recent and open, and are new to us."""
    me = reddit.user.me().name.lower()
    cutoff = now - timedelta(hours=cfg["max_thread_age_hours"])
    seen = set(state["seen"])
    found = []
    for sub in cfg["subreddits"]:
        for s in reddit.subreddit(sub).new(limit=cfg["scan_limit"]):
            created = datetime.fromtimestamp(s.created_utc, timezone.utc)
            if s.id in seen or created < cutoff:
                continue
            if s.locked or s.archived or s.over_18:
                continue
            if s.author and s.author.name.lower() == me:
                continue
            if matches_keywords(f"{s.title}\n{s.selftext}", cfg["keywords"]):
                found.append(s)
    return found


def top_comments(submission, n: int = 8) -> str:
    submission.comment_sort = "top"
    submission.comments.replace_more(limit=0)
    lines = []
    for c in submission.comments[:n]:
        body = c.body.replace("\n", " ")[:400]
        lines.append(f"- ({c.score} pts) {body}")
    return "\n".join(lines) or "(no comments yet)"


# ---------- Claude ----------

class Verdict(BaseModel):
    should_reply: bool
    reason: str
    reply: str


SYSTEM = """You help David Dunat, a Melbourne building inspector who runs DC Building \
Inspectors, take part in Reddit discussions. You decide whether he can add something \
useful to a thread, and if so you draft his reply.

Reply only when David's inspection expertise answers the person's question better than \
the existing comments do. Skip threads that are only loosely related, already well \
answered, rants, or where a sales-sounding reply would be unwelcome. When in doubt, skip.

How the reply must read:
- Answer the question first, with concrete, practical detail a homebuyer can act on \
(what to look for, what to ask, what a report should cover, what it means). Lead with \
the useful part, not with who David is.
- Plain, friendly Australian English, the way an experienced tradie talks on Reddit. \
No marketing language, no exclamation marks, no emoji, no headings, no sign-off.
- 60 to 200 words. Short paragraphs or a few dashes are fine.
- Do not tell them to book David, and do not mention prices, discounts or availability.
- Only state facts about the business that appear in the brand facts below. Never invent \
licence numbers, prices, years of experience or anecdotes.
- If the question needs a site visit to answer properly, say so honestly.
- Do not include any link and do not add a disclosure line; the system adds those.

Brand facts:
{brand}"""


def draft_reply(client, cfg: dict, brand: str, thread: dict) -> Verdict | None:
    prompt = (
        f"Subreddit: r/{thread['subreddit']}\n"
        f"Title: {thread['title']}\n\n"
        f"Post:\n{thread['body'][:4000] or '(no text)'}\n\n"
        f"Top existing comments:\n{thread['comments']}"
    )
    response = client.messages.parse(
        model=cfg["model"],
        max_tokens=16000,
        output_config={"effort": "medium"},
        system=SYSTEM.format(brand=brand),
        messages=[{"role": "user", "content": prompt}],
        output_format=Verdict,
    )
    if response.stop_reason != "end_turn" or response.parsed_output is None:
        print(f"  skipped: Claude stopped with {response.stop_reason}")
        return None
    return response.parsed_output


# ---------- commands ----------

def cmd_find() -> None:
    import anthropic

    cfg, state = load_config(), load_state()
    brand = (HERE / "brand.md").read_text()
    reddit, claude = reddit_client(), anthropic.Anthropic()
    now = datetime.now(timezone.utc)
    QUEUE.mkdir(exist_ok=True)

    threads = candidate_threads(reddit, cfg, state, now)
    print(f"{len(threads)} matching threads")
    drafted = 0
    for s in threads:
        if drafted >= cfg["max_drafts_per_run"]:
            break
        state["seen"].append(s.id)
        thread = {
            "subreddit": s.subreddit.display_name,
            "title": s.title,
            "body": s.selftext,
            "comments": top_comments(s),
        }
        verdict = draft_reply(claude, cfg, brand, thread)
        if not verdict or not verdict.should_reply:
            print(f"  no reply: {s.title[:70]} ({verdict.reason if verdict else 'n/a'})")
            continue
        draft = Draft(
            QUEUE / f"{now:%Y-%m-%d}-{s.id}.md",
            {
                "status": "pending",  # change to "approved" to post, or "rejected"
                "thread_id": s.id,
                "subreddit": thread["subreddit"],
                "title": s.title,
                "url": f"https://www.reddit.com{s.permalink}",
                "found": now.isoformat(timespec="minutes"),
                "why": verdict.reason,
                "include_link": False,  # set true to add the website link (rate-limited)
            },
            verdict.reply,
        )
        draft.write()
        drafted += 1
        print(f"  drafted: {draft.path.name}")
    save_state(state)
    print(f"{drafted} drafts saved to reddit/queue/")


def allowed_to_post(meta: dict, state: dict, cfg: dict, now: datetime) -> str | None:
    """Return a reason if posting now would break a limit, else None."""
    lim = cfg["limits"]
    posted = [(p, datetime.fromisoformat(p["at"])) for p in state["posted"]]
    today = [p for p, at in posted if at > now - timedelta(days=1)]
    if len(today) >= lim["max_replies_per_day"]:
        return "daily limit reached"
    week_sub = [
        p for p, at in posted
        if at > now - timedelta(days=7) and p["subreddit"].lower() == meta["subreddit"].lower()
    ]
    if len(week_sub) >= lim["max_replies_per_subreddit_per_week"]:
        return f"weekly limit for r/{meta['subreddit']} reached"
    return None


def link_allowed(state: dict, cfg: dict) -> bool:
    n = cfg["limits"]["link_every_n_replies"]
    recent = state["posted"][-(n - 1):] if n > 1 else []
    return not any(p.get("link") for p in recent)


def compose(body: str, meta: dict, state: dict, cfg: dict) -> tuple[str, bool]:
    text = body.strip()
    use_link = bool(meta.get("include_link")) and link_allowed(state, cfg)
    disclosure = cfg["disclosure"]
    if use_link:
        disclosure = disclosure.rstrip(".)") + f" — {cfg['website']})"
    return f"{text}\n\n{disclosure}", use_link


def cmd_post() -> None:
    cfg, state = load_config(), load_state()
    approved = [d for d in all_drafts() if d.meta.get("status") == "approved"]
    if not approved:
        print("nothing approved")
        return
    reddit = reddit_client()
    for d in approved:
        now = datetime.now(timezone.utc)
        blocked = allowed_to_post(d.meta, state, cfg, now)
        if blocked:
            print(f"  held {d.path.name}: {blocked} (will retry next run)")
            continue
        if LINK_RE.search(d.body):
            d.meta["status"] = "needs-edit"
            d.meta["note"] = "Remove links from the text; set include_link: true instead."
            d.write()
            print(f"  {d.path.name}: has a link in the body, sent back for edit")
            continue
        s = reddit.submission(id=d.meta["thread_id"])
        if s.locked or s.archived or s.removed_by_category:
            d.meta["status"] = "skipped"
            d.meta["note"] = "Thread locked, archived or removed before posting."
            d.write()
            continue
        text, used_link = compose(d.body, d.meta, state, cfg)
        comment = s.reply(text)
        d.meta.update(
            status="posted",
            posted=now.isoformat(timespec="minutes"),
            comment_url=f"https://www.reddit.com{comment.permalink}",
        )
        d.write()
        state["posted"].append({
            "thread_id": d.meta["thread_id"],
            "subreddit": d.meta["subreddit"],
            "at": now.isoformat(),
            "link": used_link,
            "comment_id": comment.id,
        })
        save_state(state)
        print(f"  posted {d.path.name}")
        time.sleep(60)  # space comments out
    save_state(state)


def main() -> None:
    cmds = {"find": cmd_find, "post": cmd_post}
    if len(sys.argv) != 2 or sys.argv[1] not in cmds:
        sys.exit(f"usage: python {Path(__file__).name} [{'|'.join(cmds)}]")
    cmds[sys.argv[1]]()


if __name__ == "__main__":
    main()
