# file_handler.py
from datetime import datetime
from models import Tab

def save_closed_tabs(tabs: list[Tab]) -> str:
    """닫은 탭을 백업 파일로 저장합니다."""
    print("\n💾 닫은 탭 백업 중...")
    
    filename = f"closed_tabs_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
    
    with open(filename, 'w', encoding='utf-8') as f:
        f.write("=" * 60 + "\n")
        f.write("🗑️  AI 탭 정리 - 닫은 탭 백업\n")
        f.write("=" * 60 + "\n\n")
        
        f.write(f"📊 총 {len(tabs)}개 탭 정리됨\n")
        f.write(f"🕐 백업 시각: {datetime.now().strftime('%Y년 %m월 %d일 %H:%M:%S')}\n")
        f.write("\n" + "=" * 60 + "\n\n")
        
        for i, tab in enumerate(tabs, 1):
            f.write(f"{i}. {tab.title}\n")
            f.write(f"   🔗 {tab.url}\n")
            
            if tab.minutesAgo is not None:
                hours = tab.minutesAgo // 60
                minutes = tab.minutesAgo % 60
                
                if hours > 0:
                    f.write(f"   ⏰ 마지막 접근: {hours}시간 {minutes}분 전\n")
                else:
                    f.write(f"   ⏰ 마지막 접근: {minutes}분 전\n")
            
            f.write("\n")
        
        f.write("=" * 60 + "\n")
        f.write("💡 팁: 이 파일을 찾아서 필요한 탭을 다시 열 수 있습니다.\n")
    
    print(f"✅ 백업 완료: {filename}")
    return filename