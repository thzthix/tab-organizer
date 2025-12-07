# browser.py
import asyncio
from playwright.async_api import async_playwright
from models import Tab

async def collect_tabs() -> list[Tab]:
    print("🔍 탭 정보 수집 중...")
    
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context()
        
        # 테스트용 탭들
        urls = [
            'https://google.com',
            'https://youtube.com',
            'https://github.com',
            'https://stackoverflow.com',
            'https://netflix.com',
        ]
        
        for url in urls:
            page = await context.new_page()
            await page.goto(url)
            await asyncio.sleep(1)
        
        # 탭 정보 수집
        tabs = []
        for page in context.pages:
            tabs.append(Tab(
                title=await page.title(),
                url=page.url
            ))
        
        await browser.close()
        
        print(f"✅ {len(tabs)}개 탭 수집 완료!")
        return tabs