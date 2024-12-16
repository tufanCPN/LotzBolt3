import pytest
from bot.utils.url_utils import extract_domain

def test_extract_domain():
    # Test cases
    test_cases = [
        ("https://www.spinco70.com/promo", "spinco"),
        ("https://bet555.com", "bet"),
        ("http://www.game123game.com", "game"),
        ("https://777casino.com", "casino"),
        ("play88.example.com", "play"),
        ("https://www.bet365.com", "bet"),
    ]
    
    for url, expected in test_cases:
        result = extract_domain(url)
        assert result == expected, f"Failed for URL {url}. Expected {expected}, got {result}"
        
def test_invalid_urls():
    invalid_urls = [
        "",
        None,
        "not-a-url",
        "http://"
    ]
    
    for url in invalid_urls:
        result = extract_domain(url)
        assert result is None, f"Expected None for invalid URL {url}, got {result}"