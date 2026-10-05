#!/usr/bin/env python3
"""Validate skill packaging and local Markdown links without network access."""

import argparse
import json
import re
from pathlib import Path
from urllib.parse import unquote, urlsplit

import yaml


class UniqueKeyLoader(yaml.SafeLoader):
    """Reject duplicate keys instead of silently accepting the last value."""


def unique_mapping(loader, node, deep=False):
    result = {}
    for key_node, value_node in node.value:
        key = loader.construct_object(key_node, deep=deep)
        if not isinstance(key, str) or key in result:
            raise ValueError("YAML keys must be unique strings")
        result[key] = loader.construct_object(value_node, deep=deep)
    return result


UniqueKeyLoader.add_constructor(
    yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG, unique_mapping
)


def validate_skill(folder):
    errors = []
    path = folder / "SKILL.md"
    if not path.is_file():
        return ["missing SKILL.md"]
    content = path.read_text(encoding="utf-8")
    match = re.match(r"\A---\n(.*?)\n---(?:\n|$)", content, re.DOTALL)
    if not match:
        return ["missing or malformed YAML frontmatter"]
    try:
        data = yaml.load(match.group(1), Loader=UniqueKeyLoader)
    except (yaml.YAMLError, ValueError) as error:
        return ["invalid YAML: {}".format(error)]
    if not isinstance(data, dict):
        return ["frontmatter must be a mapping"]
    allowed = {"name", "description", "license", "compatibility", "metadata", "allowed-tools"}
    for key in data.keys() - allowed:
        errors.append("unknown frontmatter field: {}".format(key))
    name = data.get("name")
    if (
        not isinstance(name, str)
        or not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", name)
        or len(name) > 64
        or name != folder.name
    ):
        errors.append("name must match directory and use lowercase hyphenated words (max 64)")
    description = data.get("description")
    if not isinstance(description, str) or not 1 <= len(description.strip()) <= 1024:
        errors.append("description must be a nonempty string (max 1024)")
    for key in ("license", "allowed-tools"):
        if key in data and (not isinstance(data[key], str) or not data[key].strip()):
            errors.append("{} must be a nonempty string".format(key))
    if data.get("license") == "MIT" and not (folder / "LICENSE").is_file():
        errors.append("MIT skill must bundle LICENSE for standalone distribution")
    if "compatibility" in data and (
        not isinstance(data["compatibility"], str)
        or not 1 <= len(data["compatibility"].strip()) <= 500
    ):
        errors.append("compatibility must be a nonempty string (max 500)")
    if "metadata" in data and (
        not isinstance(data["metadata"], dict)
        or any(not isinstance(value, str) for value in data["metadata"].values())
    ):
        errors.append("metadata must map string keys to string values")
    body = content[match.end():]
    if not body.strip():
        errors.append("skill instructions are empty")
    if re.search(r"\[TODO:|\[INSERT[^\]]*\]", content, re.IGNORECASE):
        errors.append("unfinished scaffold placeholder")
    return errors


def validate_links(path, root, skill_root=None):
    errors = []
    content = path.read_text(encoding="utf-8")
    # This repository uses inline Markdown links without optional title strings.
    for target in re.findall(r"(?<!!)\[[^\]\n]+\]\(([^)\n]+)\)", content):
        target = target.strip().strip("<>")
        parsed = urlsplit(target)
        if parsed.scheme or parsed.netloc or not parsed.path:
            continue
        resolved = (path.parent / unquote(parsed.path)).resolve()
        boundary = (skill_root or root).resolve()
        try:
            resolved.relative_to(boundary)
        except ValueError:
            errors.append("link escapes package: {}".format(target))
            continue
        if not resolved.exists():
            errors.append("missing local link target: {}".format(target))
    return errors


def validate_repository(root):
    errors = []
    skills_path = root / "skills"
    skill_dirs = sorted(path for path in skills_path.iterdir() if path.is_dir()) if skills_path.is_dir() else []
    if not skill_dirs:
        errors.append("no skill directories found")
    for folder in skill_dirs:
        errors.extend("{}: {}".format(folder.name, error) for error in validate_skill(folder))
    for path in sorted(root.rglob("*.md")):
        if any(part.startswith(".") for part in path.relative_to(root).parts):
            continue
        skill_root = None
        relative = path.relative_to(root)
        if len(relative.parts) >= 3 and relative.parts[0] == "skills":
            skill_root = root / "skills" / relative.parts[1]
        errors.extend(
            "{}: {}".format(relative, error)
            for error in validate_links(path, root, skill_root)
        )
    errors.extend(validate_evaluation_cases(root))
    return skill_dirs, errors


def validate_evaluation_cases(root):
    """Check that every skill has a runnable, reviewable case in the corpus."""
    cases_path = root / "evals" / "cases.json"
    if not cases_path.is_file():
        return ["missing evals/cases.json"]
    try:
        cases = json.loads(cases_path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, UnicodeError) as error:
        return ["invalid cases.json: {}".format(error)]
    if not isinstance(cases, list) or not cases:
        return ["cases.json must contain a nonempty array"]

    skill_dirs = {
        path.name for path in (root / "skills").iterdir() if path.is_dir()
    } if (root / "skills").is_dir() else set()
    eval_root = (root / "evals").resolve()
    ids = set()
    covered_skills = set()
    errors = []
    for index, case in enumerate(cases):
        label = "case {}".format(index + 1)
        if not isinstance(case, dict):
            errors.append("{} must be an object".format(label))
            continue
        case_id = case.get("id")
        if not isinstance(case_id, str) or not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", case_id):
            errors.append("{} id must be a lowercase hyphenated string".format(label))
        elif case_id in ids:
            errors.append("duplicate case id: {}".format(case_id))
        else:
            ids.add(case_id)

        skill = case.get("skill")
        if not isinstance(skill, str) or skill not in skill_dirs:
            errors.append("{} references unknown skill: {}".format(label, skill))
        else:
            covered_skills.add(skill)

        mode = case.get("mode")
        if not isinstance(mode, str) or mode not in {"review", "implementation"}:
            errors.append("{} mode must be review or implementation".format(label))

        fixture = case.get("fixture")
        if not isinstance(fixture, str) or not fixture.strip():
            errors.append("{} fixture must be a nonempty relative path".format(label))
        elif Path(fixture).is_absolute():
            errors.append("{} fixture must be a relative path: {}".format(label, fixture))
        else:
            fixture_path = (eval_root / fixture).resolve()
            try:
                fixture_path.relative_to(eval_root)
            except ValueError:
                errors.append("{} fixture escapes evals directory: {}".format(label, fixture))
            else:
                if not fixture_path.is_file():
                    errors.append("{} missing fixture: {}".format(label, fixture))

        request = case.get("request")
        if not isinstance(request, str) or not request.strip():
            errors.append("{} request must be a nonempty task instruction".format(label))
        for criterion in ("acceptance", "reject"):
            values = case.get(criterion)
            if not isinstance(values, list) or not values or any(
                not isinstance(value, str) or not value.strip() for value in values
            ):
                errors.append("{} {} must be a nonempty list of criteria".format(label, criterion))

    uncovered = sorted(skill_dirs - covered_skills)
    if uncovered:
        errors.append("evaluation corpus does not cover skills: {}".format(", ".join(uncovered)))
    return errors


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("root", nargs="?", type=Path, default=Path(__file__).resolve().parents[1])
    args = parser.parse_args()
    try:
        skills, errors = validate_repository(args.root.resolve())
    except (OSError, UnicodeError) as error:
        parser.exit(1, "Validation failed: {}\n".format(error))
    for error in errors:
        print("ERROR: {}".format(error))
    if errors:
        return 1
    print("Validated {} skills, local Markdown links, and evaluation cases. Behavior is evaluated separately.".format(len(skills)))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
