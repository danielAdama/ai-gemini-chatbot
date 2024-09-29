from fastapi import APIRouter, status, Query, Depends, Path, Request
import uuid
from src.schemas import chat_schema
from src.services import chat_service
from typing import Dict, Union, List, Annotated
from src.utils.request_response import ApiResponse

chat_router = APIRouter(prefix="/chat", tags=["Chat"])

@chat_router.post(
        '/messages/',
        response_model=Dict[str, Union[str, chat_schema.ChatSchemaOut]],
        status_code=status.HTTP_201_CREATED
    )
async def send_message(
    chat: chat_schema.ChatIn
    ):
    result = await chat_service.ChatService.ask(chat)
    return ApiResponse(
        message="Chat added successfully",
        data=result
    )