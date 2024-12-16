import asyncio
import logging
from bot.browser_handler import BrowserHandler
from bot.site_manager import SiteManager

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)

async def test_spinco():
    """Test scenario for spinco70.com"""
    browser_handler = None
    try:
        # Initialize components
        browser_handler = BrowserHandler()
        browser_handler.initialize()
        site_manager = SiteManager()
        
        # Test data
        test_url = "https://spinco70.com"
        test_code = "TEST123"  # Test promo kodu
        
        logger.info("Starting spinco70.com test scenario")
        
        # Process the promo code
        result = await site_manager.process_promo(
            browser_handler,
            test_url,
            test_code
        )
        
        if result:
            logger.info("Spinco70 test completed successfully!")
        else:
            logger.error("Spinco70 test failed!")
            
    except Exception as e:
        logger.error(f"Error in spinco70 test: {str(e)}")
    finally:
        if browser_handler:
            browser_handler.close()

if __name__ == "__main__":
    asyncio.run(test_spinco())