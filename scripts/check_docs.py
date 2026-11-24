"""Check Markdown link targets and required distribution notices."""

from pathlib import Path
from urllib.parse import unquote, urlsplit

from markdown_it import MarkdownIt

ROOT = Path(__file__).resolve().parents[1]


def main():
    files = sorted(
        [
            *ROOT.glob("*.md"),
            *(ROOT / "docs").rglob("*.md"),
            *(ROOT / "examples").glob("*.md"),
            *(ROOT / "reports").glob("*.md"),
            *(ROOT / "infra").rglob("*.md"),
            ROOT / "public-demo/README.md",
        ]
    )
    parser = MarkdownIt()
    issues = []
    for path in files:
        for token in parser.parse(path.read_text()):
            for child in token.children or []:
                target = child.attrGet("href") or child.attrGet("src")
                if not target:
                    continue
                local = urlsplit(target)
                if (
                    not local.scheme
                    and not local.netloc
                    and local.path
                    and not (path.parent / unquote(local.path)).exists()
                ):
                    issues.append(f"{path.relative_to(ROOT)} -> {target}")
    for name in (
        "LICENSE",
        "THIRD_PARTY_NOTICES.md",
        "docs/licenses/MITRE-ATTACK.txt",
        "SECURITY.md",
    ):
        if not (ROOT / name).is_file():
            issues.append(name)
    if issues:
        raise SystemExit("\n".join(issues))
    print(f"Checked local links in {len(files)} documents and required notices")


if __name__ == "__main__":
    main()
