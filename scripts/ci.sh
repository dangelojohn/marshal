#!/bin/sh
# Full gate: static checks, then a real Odoo install+test against a SCRATCH db.
#
# VERIFIED 2026-08-06: `-i --test-enable --no-http` runs happily alongside the
# LIVE server. --no-http is what prevents the port-8069 bind, so CI needs NO
# production downtime. (An earlier assumption that the server must be stopped
# was wrong — tested and disproved on the live box.)
set -u
[ -t 1 ] && { R=$(printf '\033[31m'); G=$(printf '\033[32m'); Y=$(printf '\033[33m'); Z=$(printf '\033[0m'); } || { R=""; G=""; Y=""; Z=""; }
BASE=${MARSHAL_BASE:-/share/CACHEDEV2_DATA/marshal}
export PATH=$BASE/bin:$PATH
DB="ci_marshal_$$"
cleanup() { rc=$?; docker exec marshal-db psql -U odoo -d postgres -c "DROP DATABASE IF EXISTS $DB;" >/dev/null 2>&1; exit $rc; }
trap cleanup EXIT INT TERM
P=0; N=0
step() { N=$((N+1)); printf '%s==> [%d] %s%s\n' "$Y" "$N" "$1" "$Z"; shift
         if "$@"; then P=$((P+1)); printf '%s    OK%s\n' "$G" "$Z"
         else printf '%s    FAILED%s\n' "$R" "$Z"; printf '%ssummary: %d/%d passed%s\n' "$R" "$P" "$N" "$Z"; exit 1; fi; }
step "static checks"  sh "$(dirname "$0")/lint.sh"
step "odoo install + tests on scratch db $DB" sh -c '
  LOG=$1/logs/ci-odoo.log; DB=$2
  docker exec marshal-odoo odoo -c /etc/odoo/odoo.conf -d "$DB" \
    -i marshal_core --without-demo=all --test-enable --test-tags /marshal_core \
    --stop-after-init --no-http --max-cron-threads=0 > "$LOG" 2>&1
  rc=$?
  grep -E "marshal_core: [0-9]+ tests" "$LOG" | tail -1
  # Odoo can exit 0 with failures logged, so check the log too.
  if [ $rc -ne 0 ] || grep -qE "^(FAIL|ERROR): " "$LOG"; then
    echo "--- tail ---"; tail -20 "$LOG"; exit 1
  fi' _ "$BASE" "$DB"
printf '%ssummary: %d/%d passed%s\n' "$G" "$P" "$N" "$Z"
