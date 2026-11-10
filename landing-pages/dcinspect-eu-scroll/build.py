# Embeds the images into the paste-ready files. Run: python3 build.py
import re,base64,os
def embed(s):
    imgs={k:f'img/{k}.webp' for k in ['hero','roof','pipe','damp','floor','crack','drain','newbuild']}
    for f in os.listdir('walk'): imgs[f[:-5]]='walk/'+f
    for k,p in imgs.items():
        tok=f'__IMG_{k}__'
        if tok in s: s=s.replace(tok,'data:image/webp;base64,'+base64.b64encode(open(p,'rb').read()).decode())
    s=re.sub(r'#dci \.ph-(hero|roof|pipe|damp|floor|crack|drain|new)\{background-image:url\(data:[^)]*\)\}\n','',s)
    assert not re.findall(r'__IMG_\w+__',s), re.findall(r'__IMG_\w+__',s)
    return s
for src,out in [('hero-source.html','dcinspect-eu-hero-godaddy.html'),('source.html','dcinspect-eu-godaddy.html')]:
    b=embed(open(src).read()); open(out,'w').write(b); print(out,os.path.getsize(out)//1024,'KB')
