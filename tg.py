import logging
import os

import telegram

logging.basicConfig()
logger = logging.getLogger("Telegram")
logger.setLevel(logging.DEBUG)


class TelegramBot:
    def __init__(self):
        self.bot: telegram.Bot = self._init_bot()

    @staticmethod
    def _init_bot() -> telegram.Bot:
        return telegram.Bot(os.getenv("TG_TOKEN"))

    async def send_message(self, chat_id: str, msg: str) -> None:
        logger.info("Sending message")
        await self.bot.send_message(chat_id=chat_id, text=msg)
        logger.info("Message sent")
