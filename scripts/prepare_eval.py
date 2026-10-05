#!/usr/bin/env python3
"""Export one behavioral task without its private grading criteria."""

import argparse
import hashlib
import json
from pathlib import Path

from validate import validate_evaluation_cases


def prepare_case(root, case_id):
    errors = validate_evaluation_cases(root)
    if errors:
        raise ValueError("invalid evaluation corpus: " + "; ".join(errors))
    cases = json.loads((root / "evals/cases.json").read_text(encoding="utf-8"))
    case = next((item for item in cases if item["id"] == case_id), None)
    if case is None:
        raise ValueError("unknown case id: " + case_id)
    fixture = root / "evals" / case["fixture"]
    return {
        "id": "task-" + hashlib.sha256(case["id"].encode("utf-8")).hexdigest()[:12],
        "skill_path": str((root / "skills" / case["skill"] / "SKILL.md").resolve()),
        "mode": case["mode"],
        "request": case["request"],
        "raw_fixture": fixture.read_text(encoding="utf-8"),
        "fixture_name": fixture.name,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("case_id")
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--output", type=Path, help="Write the JSON task here instead of stdout")
    args = parser.parse_args()
    try:
        task = prepare_case(args.root.resolve(), args.case_id)
        payload = json.dumps(task, indent=2, ensure_ascii=False) + "\n"
        if args.output:
            args.output.write_text(payload, encoding="utf-8")
        else:
            print(payload, end="")
    except (OSError, UnicodeError, ValueError) as error:
        parser.exit(1, "Cannot prepare task: {}\n".format(error))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
