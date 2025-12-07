from datetime import datetime
from models import TabCategories, Tab

def save_to_file(categories: TabCategories, tabs: list[Tab]) -> str:
    print("\n💾 파일 저장 중...")
    
    filename = f"tabs_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
    
    category_names = {
        'work': '💼 업무',
        'study': '📚 공부',
        'entertainment': '🎬 엔터테인먼트',
        'social': '💬 소셜미디어',
        'shopping': '🛒 쇼핑',
        'etc': '📌 기타'
    }
    
    with open(filename, 'w', encoding='utf-8') as f:
        f.write("=" * 50 + "\n")
        f.write("📂 브라우저 탭 정리 결과\n")
        f.write("=" * 50 + "\n\n")
        
        for key, name in category_names.items():
            titles = getattr(categories, key)
            if titles:
                f.write(f"{name}\n")
                f.write("-" * 30 + "\n")
                for title in titles:
                    matching_tab = next((t for t in tabs if t.title == title), None)
                    if matching_tab:
                        f.write(f"• {title}\n")
                        f.write(f"  {matching_tab.url}\n")
                f.write("\n")
    
    print(f"✅ 저장 완료: {filename}")
    return filename


def save_closed_tabs(tabs: list[Tab]) -> str:
    """닫은 탭 백업 파일 저장"""
    print("\n💾 닫은 탭 백업 중...")
    
    filename = f"closed_tabs_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
    
    with open(filename, 'w', encoding='utf-8') as f:
        f.write("=" * 50 + "\n")
        f.write("🗑️ 닫은 탭 백업\n")
        f.write("=" * 50 + "\n\n")
        
        f.write(f"총 {len(tabs)}개 탭\n")
        f.write(f"백업 시각: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        
        for tab in tabs:
            f.write(f"• {tab.title}\n")
            f.write(f"  URL: {tab.url}\n")
            if tab.minutesAgo is not None:
                f.write(f"  마지막 접근: {tab.minutesAgo}분 전\n")
            f.write("\n")
    
    print(f"✅ 백업 완료: {filename}")
    return filename