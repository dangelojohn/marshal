#!/bin/sh
# Fast, offline static checks. No database, no Docker — safe as a pre-commit hook.
# All checks run in ONE python3 process: interpreter startup dominates runtime
# for a module this size, so batching is what keeps it under a second.
set -u
[ -t 1 ] && { R=$(printf '\033[31m'); G=$(printf '\033[32m'); Z=$(printf '\033[0m'); } || { R=""; G=""; Z=""; }
find_mod() {
  [ -n "${MARSHAL_MODULE_DIR:-}" ] && { echo "$MARSHAL_MODULE_DIR"; return; }
  for c in "$PWD/__manifest__.py" "$PWD/addons/marshal_core/__manifest__.py" \
           "$PWD/marshal_core/__manifest__.py" \
           /share/CACHEDEV2_DATA/marshal/addons/marshal_core/__manifest__.py; do
    [ -f "$c" ] && { dirname "$c"; return; }
  done
  return 1
}
MOD=$(find_mod) || { echo "${R}lint: cannot locate marshal_core (set MARSHAL_MODULE_DIR)${Z}" >&2; exit 1; }
# QTS ships NO python3 at all. Rather than install one, borrow the interpreter
# from the odoo container, which certainly has it. The module is bind-mounted
# there at /mnt/extra-addons, so the path must be translated too.
PY=$(command -v python3 2>/dev/null || command -v python 2>/dev/null || true)
if [ -n "$PY" ]; then
  RUN() { "$PY" - "$MOD"; }
else
  D=${MARSHAL_BASE:-/share/CACHEDEV2_DATA/marshal}/bin/docker
  if [ -x "$D" ] && [ "$("$D" inspect -f '{{.State.Running}}' marshal-odoo 2>/dev/null)" = "true" ]; then
    CMOD="/mnt/extra-addons/$(basename "$MOD")"
    RUN() { "$D" exec -i marshal-odoo python3 - "$CMOD"; }
    echo "  (no host python — borrowing the odoo container's interpreter)"
  else
    echo "${R}lint: no python3 on the host and marshal-odoo is not running${Z}" >&2
    exit 1
  fi
fi

RUN <<'PYEOF'
import ast, csv, os, re, sys
mod = sys.argv[1]; modname = os.path.basename(os.path.normpath(mod)); errs = []
py, xml, declared = [], [], set()
namere = re.compile(r'''_name\s*=\s*['"]([a-zA-Z0-9_.]+)['"]''')
for root, dirs, files in os.walk(mod):
    dirs[:] = [d for d in dirs if d not in (".git", "__pycache__")]
    for fn in files:
        p = os.path.join(root, fn)
        if fn.endswith(".py"):
            py.append(p)
            for m in namere.finditer(open(p, encoding="utf-8").read()):
                declared.add("model_" + m.group(1).replace(".", "_"))
        elif fn.endswith(".xml"):
            xml.append(p)
for p in py:
    try: ast.parse(open(p, "rb").read(), filename=p)
    except SyntaxError as e: errs.append("py %s:%s: %s" % (p, e.lineno, e.msg))
import xml.etree.ElementTree as ET
for p in xml:
    try: ET.parse(p)
    except ET.ParseError as e: errs.append("xml %s: %s" % (p, e))
HDR = ["id","name","model_id:id","group_id:id","perm_read","perm_write","perm_create","perm_unlink"]
cp = os.path.join(mod, "security", "ir.model.access.csv")
if not os.path.isfile(cp): errs.append("csv: missing %s" % cp)
else:
    rows = list(csv.reader(open(cp, newline="", encoding="utf-8")))
    if rows and rows[0] != HDR: errs.append("csv: header mismatch")
    seen = set()
    for i, r in enumerate(rows[1:], 2):
        if not r: continue
        if len(r) != len(HDR): errs.append("csv line %d: %d cols, want %d" % (i, len(r), len(HDR))); continue
        if r[0] in seen: errs.append("csv line %d: duplicate id %r" % (i, r[0]))
        seen.add(r[0])
        ref = r[2]
        if "." in ref:
            m, _, rest = ref.partition(".")
            if m != modname: continue      # cross-module ref: no source to check
            ref = rest
        if ref not in declared: errs.append("csv line %d: %r has no _name in this module" % (i, ref))
mp = os.path.join(mod, "__manifest__.py")
try:
    d = ast.literal_eval(open(mp, encoding="utf-8").read())
    for k in ("name","version","depends","data"):
        if k not in d: errs.append("manifest: missing %r" % k)
    if not str(d.get("version","")).startswith("16.0"):
        errs.append("manifest: version %r is not 16.0.x" % d.get("version"))
    for rel in d.get("data") or []:
        if not os.path.isfile(os.path.join(mod, rel)): errs.append("manifest: missing data file %s" % rel)
except Exception as e: errs.append("manifest: %s" % e)
for e in errs: print(e)
print("lint: %s (%d py, %d xml)" % ("FAIL" if errs else "OK", len(py), len(xml)))
sys.exit(1 if errs else 0)
PYEOF
s=$?
[ $s -eq 0 ] && echo "${G}lint: passed${Z}" || echo "${R}lint: FAILED${Z}" >&2
exit $s
