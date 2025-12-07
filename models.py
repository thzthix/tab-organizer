from pydantic import BaseModel, Field

class Tab(BaseModel):
    id: int | None = None 
    title: str
    url: str
    lastAccessed: float | None  = None 
    minutesAgo: int | None  = None 

class SmartCleanupRequest(BaseModel):
    focused_tabs: list[dict]
    all_tabs: list[dict]
    time_threshold: int = 60

class TabContext(BaseModel):
    focused_tab: list[Tab]
    all_tabs: list[Tab]