import pytest
import asyncio
from bot.telegram_reader import TelegramReader
from bot.browser_handler import BrowserHandler
from bot.site_manager import SiteManager
import json

@pytest.fixture
def browser_handler():
    handler = BrowserHandler()
    handler.initialize()
    yield handler
    handler.close()

@pytest.fixture
def site_manager():
    return SiteManager()

def test_site_credentials():
    """Test if credentials are properly loaded and matched"""
    with open("config/loginData.json") as f:
        credentials = json.load(f)
    
    site_manager = SiteManager()
    test_url = "https://example-site.com/some/path"
    creds = site_manager.get_login_credentials(test_url)
    
    assert creds is not None
    assert creds["username"] == "testuser1"
    assert creds["password"] == "securepass123"

def test_site_config():
    """Test if site configuration is properly loaded"""
    site_manager = SiteManager()
    test_url = "https://example-site.com/some/path"
    config = site_manager.get_site_config(test_url)
    
    assert config is not None
    assert "login_page" in config
    assert "promo_page" in config
    assert "selectors" in config

@pytest.mark.asyncio
async def test_promo_workflow(browser_handler, site_manager):
    """Test the complete promo code workflow"""
    test_url = "https://example-site.com/promo"
    test_code = "TESTPROMO123"
    
    result = await site_manager.process_promo(
        browser_handler,
        test_url,
        test_code
    )
    
    assert result is True  # Should be True if everything worked