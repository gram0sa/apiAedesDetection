from telegram import Bot
from config.Config import Config

class TelegramNotifier:
    def __init__(self):
        self.bot_token = Config.TOKEN_TELEGRAM
        self.chat_id = Config.CHAT_ID
        self.bot = Bot(token=self.bot_token)

    async def send_photo(self, image, caption=""):
        try:
            full_caption = f"{Config.MESSAGE}\n{caption}"
            await self.bot.send_photo(chat_id=self.chat_id, photo=image, caption=full_caption)
        except Exception as e:
            print(f"Erro ao enviar imagem: {e}")
