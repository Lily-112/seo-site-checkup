thonpython
import json
import logging
from pathlib import Path
from extractors.seo_parser import SEOParser
from extractors.performance_analyzer import PerformanceAnalyzer
from extractors.security_checks import SecurityChecks
from outputs.exporters import Exporter

logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(message)s')

def load_settings():
    settings_path = Path(__file__).parent / "config" / "settings.example.json"
    try:
        with open(settings_path, "r") as f:
            return json.load(f)
    except Exception as e:
        logging.error(f"Failed to load settings: {e}")
        return {}

def run(url: str):
    logging.info(f"Running SEO audit for: {url}")

    seo = SEOParser(url)
    perf = PerformanceAnalyzer(url)
    sec = SecurityChecks(url)

    result = {
        "meta": seo.extract_meta(),
        "keywords": seo.extract_keywords(),
        "speedMetrics": perf.analyze_performance(),
        "security": sec.run_security_checks(),
    }

    Exporter.export_json(result, f"{url.replace('https://','').replace('/','_')}.json")

    logging.info("Audit completed.")
    return result

if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        logging.error("Usage: python runner.py <url>")
        exit(1)

    run(sys.argv[1])