import json
import logging
from bot.utils.url_utils import extract_domain
import time

logger = logging.getLogger(__name__)

class SiteManager:
    def __init__(self, sites_config="config/sites.json", login_data="config/login_data.json"):
        with open(sites_config) as f:
            self.sites = json.load(f)
        with open(login_data) as f:
            self.login_data = json.load(f)
            
    def get_site_config(self, url):
        """Get site configuration based on URL"""
        domain = extract_domain(url)
        if not domain:
            logger.error(f"Could not extract domain from URL: {url}")
            return None
            
        # Try exact match first
        for site_domain in self.sites:
            if extract_domain(site_domain) == domain:
                return self.sites[site_domain]
        return None
        
    def get_login_credentials(self, url):
        """Get login credentials for a specific site"""
        domain = extract_domain(url)
        if not domain:
            logger.error(f"Could not extract domain from URL: {url}")
            return None
            
        # Try exact match first
        for site_domain in self.login_data:
            if extract_domain(site_domain) == domain:
                return self.login_data[site_domain]
        return None
        
    async def process_promo(self, browser_handler, site_url, promo_code):
        """Process promotion code for a specific site"""
        try:
            site_config = self.get_site_config(site_url)
            if not site_config:
                logger.error(f"No configuration found for site: {site_url}")
                return False
                
            credentials = self.get_login_credentials(site_url)
            if not credentials:
                logger.error(f"No login credentials found for site: {site_url}")
                return False
                
            # Navigate to home page
            logger.info(f"Navigating to home page: {site_config['home_page']}")
            if not browser_handler.navigate(site_config["home_page"]):
                return False
                
            # Wait for page load and close ad if present
            logger.info("Waiting for page load...")
            time.sleep(0.05)  # Increased wait time for better stability
            
            #logger.info("Attempting to close advertisement...")
            #browser_handler.click(site_config["selectors"]["ad_close_button"], wait=False)
            #time.sleep(0.05)  # Wait after closing ad
            
            # Click login button to open login form
            logger.info("Opening login form...")
            if not browser_handler.click(site_config["selectors"]["login_open_button"]):
                logger.error("Failed to click login button")
                return False
                
            # Wait for login form
            time.sleep(0.05)
            
            # Input credentials
            logger.info("Entering login credentials...")
            if not browser_handler.find_and_input(site_config["selectors"]["username_input"], credentials["username"]):
                logger.error("Failed to input username")
                return False
                
            if not browser_handler.find_and_input(site_config["selectors"]["password_input"], credentials["password"]):
                logger.error("Failed to input password")
                return False
                
            # Submit login
            logger.info("Submitting login...")
            if not browser_handler.click(site_config["selectors"]["login_submit_button"]):
                logger.error("Failed to click login submit button")
                return False
                
            # Wait for login to complete
            logger.info("Waiting for login to complete...")
            time.sleep(0.1)
            
            browser_handler.navigate(site_config["home_page"])
            time.sleep(0.05)
            # Handle promo code submission
            if site_config.get("is_direct_promo_page", True):
                logger.info("Using direct promo page navigation...")
                if not browser_handler.navigate(site_config["promo_page"]):
                    return False
            else:
                logger.info("Using menu navigation for promo...")
                if not browser_handler.click(site_config["selectors"]["promo_menu"]):
                    logger.error("Failed to click promo menu")
                    return False

                if not browser_handler.click(site_config["selectors"]["promo_menu_button"]):
                    logger.error("Failed to click promo menu button")
                    return False
                    
                time.sleep(0.05)  # Wait for menu animation
                
                if not browser_handler.click(site_config["selectors"]["promo_submenu_button"]):
                    logger.error("Failed to click promo submenu button")
                    return False
                    
                time.sleep(0.05)  # Wait for form to load
            
            # Submit promo code
            logger.info(f"Entering promo code: {promo_code}")
            if not browser_handler.find_and_input(site_config["selectors"]["promo_input"], promo_code):
                logger.error("Failed to input promo code")
                return False
                
            logger.info("Submitting promo code...")
            if not browser_handler.click(site_config["selectors"]["promo_submit"]):
                logger.error("Failed to click promo submit button")
                return False
                
            logger.info("Promo code process completed successfully")
            return True
            
        except Exception as e:
            logger.error(f"Error processing promo: {str(e)}")
            return False