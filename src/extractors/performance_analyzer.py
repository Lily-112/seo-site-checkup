thonpython
import requests
import time
import logging

class PerformanceAnalyzer:
    def __init__(self, url: str):
        self.url = url

    def analyze_performance(self):
        metrics = {}
        try:
            start = time.time()
            resp = requests.get(self.url, timeout=10)
            load_time = time.time() - start
            size_bytes = len(resp.content)

            metrics = {
                "load_time_seconds": round(load_time, 4),
                "html_size_kb": round(size_bytes / 1024, 2),
                "status_code": resp.status_code,
            }

        except Exception as e:
            logging.error(f"Performance analysis failed: {e}")

        return metrics