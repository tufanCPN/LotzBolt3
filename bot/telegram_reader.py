from telegram.ext import Application, MessageHandler, filters
import logging
import json
import re

logger = logging.getLogger(__name__)

class TelegramReader:
    def __init__(self, config_path="config/settings.json"):
        with open(config_path) as f:
            self.config = json.load(f)
        
        self.bot = None
        self.last_message_id = None
    
    async def initialize(self):
        """Initialize the Telegram bot"""
        self.bot = Application.builder().token(self.config["telegram"]["api_token"]).build()
        
    async def get_new_messages(self):
        """Check for new messages in the specified channel"""
        try:
            messages = await self.bot.bot.get_chat_history(
                chat_id=self.config["telegram"]["channel_id"],
                limit=1
            )
            
            for message in messages:
                if self.last_message_id and message.message_id <= self.last_message_id:
                    continue
                    
                self.last_message_id = message.message_id
                return self.parse_message(message.text)
                
        except Exception as e:
            logger.error(f"Error getting messages: {str(e)}")
            return None
    
    def parse_message(self, text):
        """Parse the message text to extract code and site URL"""
        if not text:
            return None
            
        lines = text.strip().split('\n')
        if len(lines) < 3:
            return None
            
        return {
            'code': lines[0].strip(),
            'site_url': lines[2].strip()
        }