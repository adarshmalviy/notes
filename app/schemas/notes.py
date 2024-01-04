from typing import Optional, List
from pydantic import BaseModel


# Notes Create model
class NoteCreate(BaseModel):
    title: str
    content: str
    

# Notes Update model
class NoteUpdate(BaseModel):
    title: Optional[str]=None
    content: Optional[str]=None
    

class ShareToUser(BaseModel):
    recipient_username: str

class NoteSearchResult(BaseModel):
    id: int
    title: str
    content: str

class SearchNotesResponse(BaseModel):
    message: str
    search_results: List[NoteSearchResult]
    