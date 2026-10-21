# Reddit outreach — DC Building Inspectors

Goal: get DC Building Inspectors mentioned in the Reddit threads that ChatGPT,
Google AI Overviews, Perplexity and Claude read when someone asks "who should I
use for a building inspection in Melbourne?". Google and OpenAI license Reddit
content, and AI answers lean on threads where people asked a real question and
an upvoted reply answered it well.

So this bot doesn't post ads. It finds those questions and drafts the
reply an experienced inspector would give, signed with a short disclosure.
Upvoted helpful answers are what AI models pick up; removed or downvoted
promo does nothing, and a banned account loses everything it has posted.

## How it works

1. **Every morning (07:37 Melbourne)** `reddit-find` scans the subreddits in
   `config.yaml` for new threads (under 48 h old) about inspections, buying,
   cracks, termites, damp and so on. Claude reads each one plus its top
   comments, skips it unless David can add something, and otherwise drafts a
   reply. Drafts land in `reddit/queue/` with `status: pending`.
2. **You review on your phone.** Open the draft on GitHub, edit the text if
   you like, and change `status: pending` to `status: approved` (or
   `rejected`). Set `include_link: true` if a link to dcinspect.com.au would
   genuinely help the reader.
3. **Saving the change posts it.** `reddit-post` runs on that commit, posts
   the reply from David's account, and records the comment link in the draft.

Built-in limits (edit in `config.yaml`): at most 3 replies a day, 2 per
subreddit a week, a website link in no more than 1 of every 5 replies, and
a disclosure line on every reply. Replies over the daily limit wait and go
out on a later run.

## One-time setup

1. **Reddit account.** Use David's own account (e.g. `u/DCInspectDavid`)
   with the business named in the profile bio and a link to the site.
   Build some history first: a few weeks of ordinary, non-business comments.
   New accounts with low karma get auto-removed in most of these subreddits.
2. **Reddit API app.** At https://www.reddit.com/prefs/apps create an app of
   type **script**. Reddit now reviews new API apps under its Responsible
   Builder Policy, so you may have to request access and describe the use:
   "a personal script that posts my own human-approved comments, at most
   3 a day".
3. **Read each subreddit's rules** (sidebar) and remove any from
   `config.yaml` that ban businesses or self-promotion. If you're unsure,
   message the mods and ask. Many will say yes to a disclosed professional
   answering questions.
4. **GitHub secrets.** In this repo: Settings → Secrets and variables →
   Actions, add `ANTHROPIC_API_KEY`, `REDDIT_CLIENT_ID`,
   `REDDIT_CLIENT_SECRET`, `REDDIT_USERNAME`, `REDDIT_PASSWORD`.
   (The Reddit account must not have two-factor login enabled for script
   apps, or use a separate account for the bot.)
5. **Fill in `brand.md`.** Claude only states facts listed there: licence
   number, services, turnaround. The "things David often sees" list matters
   most, because specific first-hand detail is what gets upvoted.
6. The workflows run from the default branch, so they start once this is
   merged into `main`. Run "Reddit — find threads" by hand from the Actions
   tab to test it.

## Running locally

```
pip install -r reddit/requirements.txt
export ANTHROPIC_API_KEY=... REDDIT_CLIENT_ID=... REDDIT_CLIENT_SECRET=... \
       REDDIT_USERNAME=... REDDIT_PASSWORD=...
python reddit/bot.py find   # write drafts to reddit/queue/
python reddit/bot.py post   # post the approved ones
```

## What not to add

- No extra accounts posting as "happy customers" and no upvoting your own
  comments. That's vote manipulation: Reddit bans the whole network, and
  posing as a customer is misleading advertising under Australian
  Consumer Law.
- No unattended posting. Approving takes about 20 seconds a draft and
  catches the occasional reply that misreads a thread.

## Measuring it

Track whether AI answers mention the brand: ask ChatGPT, Perplexity and
Google "best building inspector Melbourne" monthly, or set up the Search
Atlas LLM-visibility tracker with those prompts. Expect it to take months.
Models pick up Reddit content on their own update cycle.
