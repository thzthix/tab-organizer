from pydantic import BaseModel, Field

class Tab(BaseModel):
    id: int | None = None 
    title: str
    url: str
    lastAccessed: float | None  = None 
    minutesAgo: int | None  = None 

class TabCategories(BaseModel):
    work: list[str] = Field(
        description='업무, 개발 도구, 문서 편집, 회의',
        default_factory=list
    )
    study: list[str] = Field(
        description='학습, 튜토리얼, 문서, 강의, 코딩',
        default_factory=list
    )
    entertainment: list[str] = Field(
        description='유튜브, 넷플릭스, 게임, 음악',
        default_factory=list
    )
    social: list[str] = Field(
        description='SNS, 메신저, 커뮤니티',
        default_factory=list
    )
    shopping: list[str] = Field(
        description='쇼핑몰, 장바구니',
        default_factory=list
    )
    etc: list[str] = Field(
        description='기타',
        default_factory=list
    )
    
    @classmethod
    def get_descriptions_text(cls) -> str:
        lines = []
        for field_name, field_info in cls.model_fields.items():
            desc = field_info.description or ""
            lines.append(f"- {field_name}: {desc}")
        return "\n".join(lines)

class SmartCleanupRequest(BaseModel):
    focused_tabs: list[dict]
    all_tabs: list[dict]
    time_threshold: int = 60

class TabContext(BaseModel):
    focused_tab: list[Tab]
    all_tabs: list[Tab]