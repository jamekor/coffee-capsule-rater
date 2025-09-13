import sys
from pathlib import Path

MAX_LINE_LENGTH = 88


def check_file(path: Path) -> list[str]:
    errors: list[str] = []
    with path.open("r", encoding="utf-8") as f:
        for lineno, line in enumerate(f, 1):
            stripped = line.rstrip("\n")
            if stripped.endswith(" "):
                errors.append(f"{path}:{lineno}: trailing whitespace")
            if len(stripped) > MAX_LINE_LENGTH:
                errors.append(
                    f"{path}:{lineno}: line too long "
                    f"({len(stripped)} > {MAX_LINE_LENGTH})"
                )
    return errors


def main() -> int:
    targets = [Path(p) for p in sys.argv[1:]]
    if not targets:
        targets = list(Path(".").rglob("*.py"))
    all_errors: list[str] = []
    for target in targets:
        if target.is_file() and target.suffix == ".py":
            all_errors.extend(check_file(target))
    for err in all_errors:
        print(err)
    return 1 if all_errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
