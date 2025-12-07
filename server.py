from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from file_handler import save_closed_tabs
from models import Tab, TabContext, SmartCleanupRequest
from agent import tab_manager_agent
import uvicorn

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.options("/smart-cleanup")
async def options_smart_cleanup():
    return JSONResponse(
        content={},
        headers={
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "POST, OPTIONS",
            "Access-Control-Allow-Headers": "*",
        }
    )

@app.post("/smart-cleanup")
async def smart_cleanup(request: SmartCleanupRequest):
    print("=" * 60)
    print(f"🤖 스마트 정리 시작")
    print(f"   활성 탭: {len(request.focused_tabs)}개")
    print(f"   전체 탭: {len(request.all_tabs)}개")
    print(f"   기준 시간: {request.time_threshold}분")
    print("=" * 60)
    
    focused_tabs = [Tab(**tab) for tab in request.focused_tabs]
    all_tabs = [Tab(**tab) for tab in request.all_tabs]
    
    # 디버깅: 활성 탭 출력
    print("\n📌 활성 탭:")
    for tab in focused_tabs:
        print(f"   - {tab.title} (ID: {tab.id})")
    
    # 디버깅: 오래된 탭 출력
    print(f"\n📌 오래된 탭 ({request.time_threshold}분 이상):")
    old_tabs = [tab for tab in all_tabs if tab.minutesAgo and tab.minutesAgo >= request.time_threshold]
    if old_tabs:
        for tab in old_tabs:
            print(f"   - {tab.title} (ID: {tab.id}, {tab.minutesAgo}분 전)")
    else:
        print("   → 없음! (모든 탭이 최근에 접근됨)")
    
    # 디버깅: 모든 탭의 minutesAgo 확인
    print(f"\n📊 전체 탭 상태:")
    for tab in all_tabs[:5]:  # 처음 5개만
        print(f"   - {tab.title}: {tab.minutesAgo}분 전")
    if len(all_tabs) > 5:
        print(f"   ... 외 {len(all_tabs) - 5}개")
    
    context = TabContext(
        focused_tab=focused_tabs,
        all_tabs=all_tabs
    )
    
    message = f"현재 활성 탭 기반으로 {request.time_threshold}분 이상 안 본 관련 없는 탭을 정리해주세요."
    print(f"\n🤖 Agent에게 전달하는 메시지:")
    print(f"   {message}")
    
    result = await tab_manager_agent.run(message, deps=context)
    
    print(f"\n✅ Agent 응답:")
    print(f"   타입: {type(result.output)}")
    print(f"   내용: {result.output}")
    
    tab_ids = result.output
    print(f"\n📊 최종 결과: {len(tab_ids)}개 탭 정리 예정")
    
    if tab_ids:
        tabs_to_close = [tab for tab in all_tabs if tab.id in tab_ids]
        print(f"\n🗑️ 닫을 탭:")
        for tab in tabs_to_close:
            print(f"   - {tab.title} (ID: {tab.id})")
        
        backup_file = save_closed_tabs(tabs_to_close)
        print(f"\n💾 백업: {backup_file}")
    else:
        print("\n❌ 닫을 탭이 없습니다")
    
    print("=" * 60)
    
    return {
        "success": True,
        "tab_ids": tab_ids
    }

if __name__ == "__main__":
    print("=" * 50)
    print("🚀 탭 정리 서버 시작")
    print("=" * 50)
    print("📍 주소: http://localhost:8000")
    print("🤖 /smart-cleanup - 스마트 정리")
    print("=" * 50)
    uvicorn.run(app, host="localhost", port=8000, log_level="info")
