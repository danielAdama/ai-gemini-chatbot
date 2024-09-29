from fastapi import status, Request
import uuid
from datetime import datetime as dt
from typing import Union, Dict, Optional
from pathlib import Path
from src.schemas import chat_schema
from src.exceptions.custom_exception import (
    APIAuthenticationFailException, InternalServerException, RecordNotFoundException
)
from gen_ai import AITeacher
from src.utils.app_utils import AppUtil
from src.utils.app_notification_message import NotificationMessage

from config.logger import Logger

logger = Logger(__name__)

class ChatService:
    BASE_DIR = Path(__file__).absolute().parent.parent.parent
    PROMPT_DIR = BASE_DIR / "gen_ai" / "prompt" / "templates"

    @staticmethod
    async def ask(
        chat: chat_schema.ChatIn,
        system_template = AppUtil.load_file(PROMPT_DIR / "system_template.txt")
    ):
        chat_dict = chat.model_dump()
        # try:
        chatbot=AITeacher(
            system_prompt=system_template
        )
        result = chatbot.run_conversation(chat_dict["question"])

        logger.info("Chats processed successfully")
            
        # except Exception as ex:
        #     logger.error(f"Creating Train -> API /train/: {ex}")
        #     raise InternalServerException()
        
        return result