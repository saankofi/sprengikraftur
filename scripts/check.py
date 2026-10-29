"""Checks skill frontmatter and relative links in the repo's Markdown."""

import re
import sys
from pathlib import Path

root = Path(__file__).resolve().parent.parent
errors = []

for skill in sorted(root.glob("skills/*/SKILL.md")):
    text = skill.read_text()
    match = re.match(r"---\n(.*?)\n---\n", text, re.S)
    if not match:
        errors.append(f"{skill.relative_to(root)}: no frontmatter")
        continue
    fields = dict(
        line.split(":", 1) for line in match.group(1).splitlines() if ":" in line
    )
    name = fields.get("name", "").strip()
    if name != skill.parent.name:
        errors.append(f"{skill.relative_to(root)}: name '{name}' doesn't match its folder")
    if not fields.get("description", "").strip():
        errors.append(f"{skill.relative_to(root)}: no description")

for doc in sorted(root.rglob("*.md")):
    if ".git" in doc.parts:
        continue
    for target in re.findall(r"\]\(([^)\s]+)\)", doc.read_text()):
        if re.match(r"[a-z]+:", target) or target.startswith("#"):
            continue
        if not (doc.parent / target.split("#")[0]).exists():
            errors.append(f"{doc.relative_to(root)}: broken link {target}")

print("\n".join(errors) or "ok")
sys.exit(1 if errors else 0)
