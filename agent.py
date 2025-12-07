# agent.py
from dotenv import load_dotenv
from pydantic_ai import Agent, RunContext
from models import TabContext, TabCategories

load_dotenv()

tab_manager_agent = Agent(
    'google-gla:gemini-2.0-flash-exp',
    deps_type=TabContext,
    output_type=list[int],
    instructions=f'''
    당신은 카테고리 기반 탭 정리 전문가입니다.
    
    [카테고리 기준]
    {TabCategories.get_descriptions_text()}
    
    [정리 절차]
    1. focused_tab들을 각각 카테고리로 분류하세요
    2. find_old_tabs()로 오래된 탭 목록을 가져오세요
    3. 오래된 탭들 중에서:
       - focused_tab과 다른 카테고리 → 모두 닫기
       - 같은 카테고리더라도 주제가 완전히 다름 → 닫기
    
    [예시]
    현재 탭: "Google Gemini" (study), "GitHub" (work)
    → study, work 카테고리는 유지
    → entertainment, social, shopping, etc → 모두 닫기
    
    [출력]
    닫을 탭 ID 리스트만 반환. 예: [1, 2, 3]
    '''
)

@tab_manager_agent.tool
async def find_old_tabs(ctx: RunContext[TabContext], minutes: int = 60) -> list[dict]:
    all_tabs = ctx.deps.all_tabs
    old = [tab for tab in all_tabs if tab.minutesAgo and tab.minutesAgo >= minutes]
     
    return [
        {'id': t.id, 'title': t.title, 'minutesAgo': t.minutesAgo}
        for t in old
    ]
