import re

def extract_domain(url):
    """
    Extract clean domain name from URL by:
    1. Removing protocol (https://)
    2. Removing www.
    3. Removing .com and anything after
    4. Removing any numbers from start and end
    
    Example:
    https://www.spinco70.com/promo -> spinco
    https://bet555.com -> bet
    """
    try:
        # Remove protocol
        domain = url.split('://')[-1]
        
        # Remove www. if exists
        if domain.startswith('www.'):
            domain = domain[4:]
            
        # Get domain part before first slash or dot
        domain = re.split(r'[./]', domain)[0]
        
        # Remove numbers from start and end
        domain = re.sub(r'^\d+|\d+$', '', domain)
        
        return domain.lower()
    except Exception as e:
        return None