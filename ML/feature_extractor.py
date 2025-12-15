# feature_extractor.py
from urllib.parse import urlparse
import tldextract
import re

def extract_features(url):
    # Normalize URL
    if not url.startswith(("http://", "https://")):
        url = "http://" + url

    # Parse URL safely
    parsed = urlparse(url)
    host = parsed.netloc.lower()

    if host.startswith("www."):
        host = host[4:]  # Remove www for consistency

    # Extract TLD safely
    tld_info = tldextract.extract(url)
    domain = tld_info.domain.lower()
    suffix = tld_info.suffix.lower()

    # Keyword-based phishing indicators
    phishing_keywords = [
        "secure", "login", "account", "update", "verify",
        "banking", "alert", "refund", "password", "recover",
        "support", "security", "billing"
    ]

    keyword_flag = 0
    for kw in phishing_keywords:
        if kw in url.lower():
            keyword_flag = 1
            break

    # Feature set
    features = {
        "length_url": len(url),

        "host_length": len(host),
        "dot_count": url.count("."),

        "has_at": 1 if "@" in url else 0,
        "suspicious_double_slash": 1 if "//" in parsed.path else 0,

        "uses_https": 1 if url.startswith("https") else 0,
        "hyphen_in_host": 1 if "-" in host else 0,

        "numeric_domain": 1 if any(c.isdigit() for c in domain) else 0,
        "digit_count": sum(c.isdigit() for c in url),
        "uppercase_count": sum(c.isupper() for c in url),

        "suspicious_tld": 1 if suffix in ["xyz", "top", "loan", "click", "live", "download"] else 0,

        "subdomain_depth": host.count("."),

        "keyword_flag": keyword_flag
    }

    return features
