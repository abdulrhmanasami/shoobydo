import os
import re
import csv
import json
import sys
import unicodedata


ROOT = "/Users/abdulrahman/Documents/GitHub/shoobydo"
MAXLEN = 80


def slugify(text: str) -> str:
    """Convert arbitrary text to a safe ASCII slug (lowercase, hyphen-separated)."""
    text = unicodedata.normalize("NFKD", text)
    text = text.encode("ascii", "ignore").decode("ascii")
    text = text.lower()
    text = re.sub(r"[^a-z0-9]+", "-", text).strip("-")
    text = re.sub(r"-{2,}", "-", text)
    return text or "untitled"


def md_title_slug(md_path: str) -> str | None:
    """Read first H1 from a Markdown file and return its slug, if found."""
    try:
        with open(md_path, "r", encoding="utf-8", errors="ignore") as f:
            for line in f:
                if line.lstrip().startswith("#"):
                    title = line.lstrip("#").strip()
                    return slugify(title)[:60]
    except Exception:
        return None
    return None


def collect_paths(root: str) -> list[str]:
    all_paths: list[str] = []
    for dirpath, dirnames, filenames in os.walk(root, topdown=True):
        dirnames[:] = [d for d in dirnames if d not in {".git", "__pycache__"}]
        for name in dirnames + filenames:
            all_paths.append(os.path.join(dirpath, name))
    return all_paths


def build_new_name(path: str, used: set[str]) -> str:
    base = os.path.basename(path)
    parent = os.path.dirname(path)
    stem, ext = os.path.splitext(base)

    # Prefer semantic slug for Markdown using H1
    if ext.lower() == ".md":
        tslug = md_title_slug(path)
        new_stem = tslug if tslug else slugify(stem)
    else:
        new_stem = slugify(stem)

    # Sanitize extension to ascii
    ext_final = ext.lower()
    if ext_final:
        ext_clean = slugify(ext_final[1:])
        ext_final = ("." + ext_clean) if ext_clean else ""

    base_candidate = new_stem + ext_final
    if len(base_candidate) > MAXLEN:
        keep = MAXLEN - len(ext_final)
        if keep < 1:
            keep = 1
        base_candidate = new_stem[:keep] + ext_final

    candidate = os.path.join(parent, base_candidate)
    counter = 2
    while (candidate in used) or (
        os.path.exists(candidate)
        and os.path.abspath(candidate) != os.path.abspath(path)
    ):
        s, e = os.path.splitext(base_candidate)
        candidate = os.path.join(parent, f"{s}-{counter}{e}")
        counter += 1
    return candidate


def main() -> int:
    all_paths = collect_paths(ROOT)
    # Map of original absolute path -> new absolute path
    rename_map: dict[str, str] = {}
    used: set[str] = set()

    # Decide renames (deeper paths first)
    for p in sorted(all_paths, key=lambda s: s.count(os.sep), reverse=True):
        base = os.path.basename(p)
        ascii_ok = all(ord(c) < 128 for c in base)
        too_long = len(base) > MAXLEN
        if ascii_ok and not too_long:
            used.add(p)
            continue
        newp = build_new_name(p, used)
        rename_map[p] = newp
        used.add(newp)

    # Rename files first
    for old, new in list(rename_map.items()):
        if os.path.isdir(old):
            continue
        os.makedirs(os.path.dirname(new), exist_ok=True)
        try:
            os.replace(old, new)
        except Exception as e:
            print(f"[WARN] file rename failed: {old} -> {new} :: {e}", file=sys.stderr)

    # Then rename directories (deepest first)
    dirs = [p for p in rename_map if os.path.isdir(p)]
    for old in sorted(dirs, key=lambda s: s.count(os.sep), reverse=True):
        new = rename_map[old]
        os.makedirs(os.path.dirname(new), exist_ok=True)
        try:
            os.replace(old, new)
        except Exception as e:
            print(f"[WARN] dir rename failed: {old} -> {new} :: {e}", file=sys.stderr)

    # Build relative map for link rewriting
    rel_map = {os.path.relpath(k, ROOT): os.path.relpath(v, ROOT) for k, v in rename_map.items()}

    # Update links within Markdown files
    link_pat = re.compile(r"(!?\[[^\]]*\]\()([^\)]+)(\))")

    def rewrite_links(md_abs: str) -> None:
        changed = False
        try:
            with open(md_abs, "r", encoding="utf-8", errors="ignore") as f:
                text = f.read()

            def _sub(m: re.Match[str]) -> str:
                nonlocal changed
                prefix, link, suffix = m.groups()
                target = link.strip()
                if target.startswith(("http://", "https://", "#")):
                    return m.group(0)
                abs_target = os.path.normpath(os.path.join(os.path.dirname(md_abs), target))
                rel_from_root = os.path.relpath(abs_target, ROOT)
                if rel_from_root in rel_map:
                    new_rel_abs = os.path.join(ROOT, rel_map[rel_from_root])
                    new_rel = os.path.relpath(new_rel_abs, os.path.dirname(md_abs))
                    changed = True
                    return f"{prefix}{new_rel}{suffix}"
                return m.group(0)

            new_text = link_pat.sub(_sub, text)
            if changed:
                with open(md_abs, "w", encoding="utf-8") as f:
                    f.write(new_text)
        except Exception as e:
            print(f"[WARN] link update failed: {md_abs} :: {e}", file=sys.stderr)

    for dirpath, _, filenames in os.walk(ROOT):
        for fn in filenames:
            if fn.lower().endswith(".md"):
                rewrite_links(os.path.join(dirpath, fn))

    # Persist maps
    with open(os.path.join(ROOT, "rename-map.csv"), "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["old_path", "new_path"])
        for old, new in sorted(rename_map.items()):
            w.writerow([os.path.relpath(old, ROOT), os.path.relpath(new, ROOT)])

    with open(os.path.join(ROOT, "rename-map.json"), "w", encoding="utf-8") as f:
        json.dump({os.path.relpath(k, ROOT): os.path.relpath(v, ROOT) for k, v in rename_map.items()}, f, ensure_ascii=False, indent=2)

    print(f"RENAMED: {len(rename_map)} items")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())


