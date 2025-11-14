thonpython
import json
from pathlib import Path
import logging

class Exporter:
    @staticmethod
    def export_json(data, filename: str):
        path = Path.cwd() / "reports"
        path.mkdir(exist_ok=True)
        try:
            with open(path / filename, "w") as f:
                json.dump(data, f, indent=4)
            logging.info(f"Report saved to reports/{filename}")
        except Exception as e:
            logging.error(f"Failed to save JSON: {e}")