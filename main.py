import asyncio
import logging
from bot.telegram_reader import TelegramReader
from bot.browser_handler import BrowserHandler
from bot.site_manager import SiteManager
import schedule
import time

# Configure logging
logging.basicConfig(
    filename='logs/bot.log',
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)

async def process_new_messages():
    """Main function to process new Telegram messages"""
    try:
        telegram_reader = TelegramReader()
        await telegram_reader.initialize()
        
        browser_handler = BrowserHandler()
        if not browser_handler.status:
            browser_handler.initialize()
        
        site_manager = SiteManager()
        
        message_data = await telegram_reader.get_new_messages()
        if message_data:
            real_url = browser_handler.get_real_url(message_data['site_url'])
            await site_manager.process_promo(
                browser_handler,
                real_url,
                message_data['code']
            )
            
    except Exception as e:
        logger.error(f"Error in main process: {str(e)}")
    finally:
        if browser_handler:
            browser_handler.close()

def run_bot():
    """Run the bot with scheduling"""
    asyncio.run(process_new_messages())

if __name__ == "__main__":
    # Schedule the bot to run every minute
    schedule.every(1).minutes.do(run_bot)
    
    while True:
        schedule.run_pending()
        time.sleep(1)