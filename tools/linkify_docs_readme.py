import re, pathlib, sys
p = pathlib.Path('docs/README.md')
if not p.exists():
    sys.exit(0)

txt = p.read_text(encoding='utf-8')
# يلتقط: "- file.md: desc" أو "* file.md" أو "1. file.md: desc"
pat = re.compile(r'(?m)^(?P<indent>\s*)(?:[-*]|\d+\.)\s+(?P<name>[A-Za-z0-9_.\-\/]+\.md)(?P<trail>\s*:\s*.*)?\s*$')

def repl(m):
    indent = m.group('indent') or ''
    name = m.group('name').strip()
    trail = m.group('trail') or ''
    return f"{indent}- [{name}]({name}){trail}"

new = pat.sub(repl, txt)
if new != txt:
    p.write_text(new, encoding='utf-8')
    print('UPDATED')
else:
    print('NOCHANGE')
