thonpython
import ssl
import socket
import logging
from urllib.parse import urlparse
import requests

class SecurityChecks:
    def __init__(self, url: str):
        self.url = url
        self.parsed = urlparse(url)

    def _check_ssl(self):
        try:
            hostname = self.parsed.hostname
            ctx = ssl.create_default_context()
            with socket.create_connection((hostname, 443), timeout=5) as sock:
                with ctx.wrap_socket(sock, server_hostname=hostname) as ssock:
                    cert = ssock.getpeercert()
            return {"ssl_valid": True, "issuer": cert.get('issuer')}
        except Exception:
            return {"ssl_valid": False}

    def _check_https(self):
        return {"uses_https": self.url.startswith("https://")}

    def _check_safe_browsing(self):
        try:
            resp = requests.get(self.url, timeout=10)
            return {"reachable": True, "status_code": resp.status_code}
        except Exception:
            return {"reachable": False}

    def run_security_checks(self):
        return {
            "ssl": self._check_ssl(),
            "https": self._check_https(),
            "safe_browsing": self._check_safe_browsing(),
        }