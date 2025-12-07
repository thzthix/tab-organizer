# main.py
import asyncio
from browser import collect_tabs
from classifier import classify_tabs
from file_handler import save_to_file

async def main():
    print("🚀 탭 정리 에이전트 시작!\n")
    
    # 1. 탭 수집
    tabs = await collect_tabs()
    
    # 2. AI 분류
    categories = await classify_tabs(tabs)
    
    # 3. 결과 출력
    print("\n📊 분류 결과:")
    print(f"  💼 업무: {len(categories.work)}개")
    print(f"  📚 공부: {len(categories.study)}개")
    print(f"  🎬 엔터테인먼트: {len(categories.entertainment)}개")
    print(f"  💬 소셜미디어: {len(categories.social)}개")
    print(f"  🛒 쇼핑: {len(categories.shopping)}개")
    print(f"  📌 기타: {len(categories.etc)}개")
    
    # 4. 파일 저장
    filename = save_to_file(categories, tabs)
    
    print(f"\n🎉 완료! 결과는 {filename}에 저장되었습니다!")

if __name__ == "__main__":
    asyncio.run(main())
