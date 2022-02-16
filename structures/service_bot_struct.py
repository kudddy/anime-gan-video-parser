from pydantic import BaseModel, Field
from typing import List, Optional


class GetFileResult(BaseModel):
    file_id: str
    file_unique_id: str
    file_size: Optional[int] = None
    file_path: Optional[str] = None


class GetFile(BaseModel):
    ok: bool
    result: GetFileResult
