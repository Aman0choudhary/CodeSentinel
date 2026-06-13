from pathlib import Path
import json


def generate_json(report: dict, output_path: Path) -> None:
    output_path.write_text(json.dumps(report, indent=2), encoding="utf-8")
