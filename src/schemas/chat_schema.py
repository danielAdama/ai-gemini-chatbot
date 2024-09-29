from pydantic import BaseModel, Field
from typing import List, Dict
from datetime import datetime as dt
from uuid import UUID, uuid4
from typing import Optional, Union
from src.utils.base import BaseSchema

#-------------------------------------------------------chatsessionschema---------------------------------------------------------
class RetreiveSchema(BaseSchema):
    user_id: str
    session_id: Optional[Union[UUID, str]] = Field(default=None, hidden=True)

class ChatIn(BaseSchema):
    question: str
    user_id: str
    session_id: Optional[Union[UUID, str]] = Field(default=None, hidden=True)

class ChatSessionSchema(BaseSchema):
    user_id: str
    title: Optional[str] = Field(default="New Chat", hidden=True)
    date_created: dt = Field(default_factory=lambda: dt.now().isoformat())
    last_modified: dt = Field(default_factory=lambda: dt.now().isoformat(), hidden=True)
    
class ChatSessionSchemaIn(ChatSessionSchema):
    id: Union[UUID, str] = Field(default_factory=uuid4, primary_key=True, hidden=True)


#-------------------------------------------------------chatschema---------------------------------------------------------
class ChatSchema(BaseSchema):
    user_id: str
    title: str
    date_created: dt
    last_modified: dt

class ChatSchemaIn(ChatSchema):
    id: Union[UUID, str] = Field(default_factory=uuid4, primary_key=True)

class ChatSchemaOut(ChatSchema):
    id: Union[UUID, str]