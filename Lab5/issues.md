# Issues

Line numbers refer to the original `address_book.py`, taken from the *before* reports (`bandit_before.txt`, `pylint_before.txt`, `flake8_before.txt`).

## Bandit (security)

| Issue | Type | Line(s) | Description | Fix Approach |
|-------|------|---------|-------------|--------------|
| Weak MD5 hash (B324, High) | Security | 19 | MD5 is broken; used to build the contact ID. | Switched to `hashlib.sha256`. |
| Unsafe pickle load (B301, Medium) | Security | 67 | `pickle.load` can run arbitrary code from a tampered backup file. | Replaced with `json.load`; backup is now `contacts.json`. |
| Pickle import (B403, Low) | Security | 3 | Importing pickle flagged as risky. | Removed pickle (also in `dump`, line 62); `import json`. |
| Hardcoded password (B105, Low) | Security | 6 | `SYNC_PASSWORD` stored in source and never used. | Deleted the unused constant. |

## Pylint (code quality)

| Issue | Type | Line(s) | Description | Fix Approach |
|-------|------|---------|-------------|--------------|
| Missing docstrings (C0114, C0116) | Style | 1, 10, 18, 22, 30, 39, 47, 53, 60, 65, 70 | Module and all 10 functions undocumented. | Added a module docstring and one per function. |
| Naming style (C0103) | Style | 10, 18, 22, 30, 39, 47, 53, 60, 65 | camelCase function and argument names. | Renamed to snake_case and updated calls in `main()`. |
| Broad except (W0718) | Bug | 34 | `except Exception` hides unrelated errors. | Narrowed to `except KeyError`. |
| range(len()) loop (C0200) | Style | 49 | Index-based loop over a list. | Used `enumerate(names, 1)`. |
| No file encoding (W1514) | Bug | 54 | `open()` depends on the system default encoding. | Added `encoding="utf-8"` to all `open()` calls. |

## Flake8 (formatting)

| Issue | Type | Line(s) | Description | Fix Approach |
|-------|------|---------|-------------|--------------|
| Missing space around operator (E225) | Style | 23 | `found=[]` | Changed to `found = []`. |
| Too many blank lines (E303) | Style | 47 | Three blank lines before a function. | Reduced to two. |
| Missing space after comma (E231) | Style | 84 | `"\| first:",sorted(...)` | Added a space after the comma. |
| Line too long (E501) | Style | 85 | 86 characters (limit 79). | Stored the comparison in a variable, then printed it. |

## Results

| Tool | Before | After |
|------|--------|-------|
| Bandit | 4 issues (1 High, 1 Medium, 2 Low) | 0 issues |
| Pylint | 5.47 / 10 | 10.00 / 10 |
| Flake8 | 4 issues | 0 issues |

I also added an `if __name__ == "__main__":` guard so importing the file no longer runs the demo. The program output is unchanged after every commit.
