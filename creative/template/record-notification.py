import asyncio, pathlib
from playwright.async_api import async_playwright
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(executable_path='/opt/pw-browsers/chromium',args=['--no-sandbox','--allow-file-access-from-files'])
        ctx=await b.new_context(viewport={'width':390,'height':844},record_video_dir='recn',record_video_size={'width':390,'height':844})
        pg=await ctx.new_page(); await pg.goto('file://'+str(pathlib.Path('notif.html').resolve())); await pg.wait_for_timeout(2600)
        await ctx.close(); await b.close()
asyncio.run(main())
