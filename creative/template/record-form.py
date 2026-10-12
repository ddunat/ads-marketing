import asyncio
from playwright.async_api import async_playwright
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(executable_path='/opt/pw-browsers/chromium',args=['--no-sandbox'])
        ctx=await b.new_context(viewport={'width':390,'height':760},device_scale_factor=2,record_video_dir='rec',record_video_size={'width':780,'height':1520},has_touch=True,is_mobile=True)
        pg=await ctx.new_page()
        await pg.goto('https://inspection.dcinspect.com.au/home-869758',wait_until='networkidle',timeout=60000)
        await pg.wait_for_timeout(1200)
        el=await pg.query_selector('input[type=radio]')
        box=await el.bounding_box()
        target=box['y']-150
        for i in range(12):
            await pg.evaluate(f'window.scrollBy(0,{target/12})'); await pg.wait_for_timeout(45)
        await pg.wait_for_timeout(500)
        for val in ["I'm buying a House","Building and/or Timber Pest Inspection","ASAP / Contract Pending"]:
            r=pg.locator(f'input[type=radio][value="{val}"]')
            await r.scroll_into_view_if_needed()
            await pg.wait_for_timeout(350)
            bb=await r.bounding_box()
            await pg.evaluate('''([x,y])=>{const d=document.createElement('div');d.style.cssText=`position:fixed;left:${x-22}px;top:${y-22}px;width:44px;height:44px;border-radius:50%;background:rgba(52,131,250,.45);border:3px solid #fff;box-shadow:0 0 0 6px rgba(52,131,250,.35);z-index:99999;pointer-events:none;transition:transform .25s,opacity .5s`;document.body.appendChild(d);setTimeout(()=>{d.style.transform='scale(1.6)';d.style.opacity='0'},350);setTimeout(()=>d.remove(),900)}''',[bb['x']+bb['width']/2,bb['y']+bb['height']/2])
            await r.click(force=True)
            await pg.wait_for_timeout(700)
        await pg.wait_for_timeout(1200)
        await ctx.close(); await b.close()
asyncio.run(main())
