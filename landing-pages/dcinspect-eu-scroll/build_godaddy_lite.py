# Builds dcinspect-eu-hero-godaddy-lite.html: under GoDaddy's 51,200-character HTML limit.
# Images load from jsDelivr (public CDN for this public GitHub repo), pinned to a commit.
import re,sys
COMMIT=sys.argv[1] if len(sys.argv)>1 else '292fec433a0e66996dc7f677bc3ed37134afa8f5'
BASE=f'https://cdn.jsdelivr.net/gh/ddunat/ads-marketing@{COMMIT}/landing-pages/dcinspect-eu-scroll/walk/'
s=open('hero-source.html').read()
s=re.sub(r'__IMG_(\w+)__',lambda m:BASE+m.group(1)+'.webp',s)
# drop rules for images not used in the hero
s=re.sub(r'#dci \.ph-(hero|roof|pipe|damp|floor|crack|drain|new)\{background-image:url\([^)]*\)\}\n','',s)
s=re.sub(r'<!--.*?-->','',s,flags=re.S)
def css_min(c):
    c=re.sub(r'/\*.*?\*/','',c,flags=re.S)
    c=re.sub(r'\s+',' ',c)
    c=re.sub(r'\s*([{};,>])\s*',r'\1',c)
    c=re.sub(r':\s+',':',c)
    c=c.replace(';}','}')
    return c.strip()
s=re.sub(r'<style>(.*?)</style>',lambda m:'<style>'+css_min(m.group(1))+'</style>',s,flags=re.S)
def js_min(j):
    lines=[]
    for ln in j.split('\n'):
        t=ln.strip()
        if not t or t.startswith('/*') and t.endswith('*/'): continue
        lines.append(t)
    return '\n'.join(lines)
s=re.sub(r'<script>(.*?)</script>',lambda m:'<script>'+js_min(m.group(1))+'</script>',s,flags=re.S)
# html: remove indentation-only whitespace between tags, keep single spaces inside text
parts=re.split(r'(<style>.*?</style>|<script>.*?</script>)',s,flags=re.S)
out=[]
for p in parts:
    if p.startswith('<style>') or p.startswith('<script>'): out.append(p); continue
    p=re.sub(r'>\s*\n\s*<','><',p)
    p=re.sub(r'\s*\n\s*',' ',p)
    p=re.sub(r' {2,}',' ',p)
    out.append(p)
s=''.join(out).strip()
open('dcinspect-eu-hero-godaddy-lite.html','w').write(s)
print('characters:',len(s),'(limit 51200)')
