from dotenv import load_dotenv
from pydantic_ai import Agent, RunContext
from models import TabContext
load_dotenv()
tab_manager_agent = Agent(
    'google-gla:gemini-2.0-flash-exp',
    deps_type=TabContext,
    output_type=list[int],
    instructions='''
    당신은 탭 정리 전문 AI입니다.
    
    [작업 절차]
    1. analyze_active_tabs()로 현재 활성 탭들의 내용과 주제 파악
    2. find_old_tabs()로 오래된 탭 목록 조회
    3. 각 오래된 탭을 분석하여 활성 탭들과의 관련성 판단
    
    [관련성 판단 기준]
    - 같은 프로젝트/주제인가? (예: 둘 다 React 관련)
    - 작업 흐름상 연결되는가? (예: 참고 문서 → 코딩)
    - 같은 학습/연구 세션인가?
    
    [주의사항]  
    - URL 도메인만으로 판단하지 마세요
    - title과 url을 종합적으로 고려하세요
    - 애매하면 유지하는 쪽으로 (실수로 닫는 게 더 나쁨)
    
    관련 없는 탭의 ID만 리스트로 반환하세요.
    '''
)

@tab_manager_agent.tool
async def analyze_active_tabs(ctx: RunContext[TabContext]) -> dict:
    focused = ctx.deps.focused_tab
    
    return {
        'count': len(focused),
        'tabs': [
            {
                'title': tab.title,
                'url': tab.url
            }
            for tab in focused
        ]
    }

@tab_manager_agent.tool
async def find_old_tabs(ctx: RunContext[TabContext], minutes: int = 60) -> list[dict]:
    all_tabs = ctx.deps.all_tabs
    old = [tab for tab in all_tabs if tab.minutesAgo and tab.minutesAgo >= minutes]
    
    return [
        {
            'id': t.id,
            'title': t.title,
            'url': t.url,
            'minutesAgo': t.minutesAgo
        }
        for t in old
    ]