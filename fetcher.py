import requests
import threading
import re
import validators


class Webcrawler(threading.Thread):
    def __init__(self, url: str, threads: int = 8, timeout: int = 10):
        threading.Thread.__init__(self)
        self.url = url
        self.threads = threads
        self.timeout = timeout
        self.addresses: list[str, ...] = []
        self.email_addresses: list[str, ...] = []

        # Requests Session
        self.session = requests.Session()
        self.session.headers = {
            "User-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36"
        }

    def run(self):
        # Regex for taking URL with HTTPS and HTTP Protocol from HTML
        pattern = r"(http[s]?:\/\/[^\s\">]+)(?<![\">])"
        
        email_pattern = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b"

        # Get HTML from URL
        content = self.session.get(self.url, timeout=self.timeout).text

        # Get Email Addresses from HTML
        self.email_addresses = re.findall(email_pattern, content)

        # Filter the data.
        addresses = re.findall(pattern, content)
        
        for address in addresses:
            if address in self.addresses:
                continue
            else:
                self.addresses.append(address)

    def join(self):
        threading.Thread.join(self)
        return (self.addresses, self.email_addresses)
