#!/usr/bin/env bash
# Run the CN v1.6.2 China transport model: LP cases and bounded hub search, Monte Carlo, gas supply, regional screen,
# seafood cross-feed, petroleum break-even, nutrient and soil-carbon balance, tests and figures.
# Flat layout: everything is read from and written to this folder.
# Usage: bash run_all.sh [monte_carlo_draws] [--no-figures]   (default 1000 draws, figures on; ~25 min on one core)
set -euo pipefail
export PYTHONDONTWRITEBYTECODE=1   # keep the folder flat (no __pycache__)
cd "$(dirname "$0")"
N="${1:-1000}"
FIGS=1
for a in "$@"; do [ "$a" = "--no-figures" ] && FIGS=0; done
[[ "$N" =~ ^[0-9]+$ ]] || N=1000
python3 cn_htse_heat.py > cn_htse_heat_log.txt
python3 cn_model.py "$N" | tee run_log.txt
python3 cn_gas.py > cn_gas_run_log.txt
python3 cn_regions.py > cn_regions_run_log.txt
python3 cn_crossfeed.py | tee cn_crossfeed_run_log.txt
python3 cn_breakeven.py
python3 cn_lull.py > cn_lull_log.txt
python3 cn_us_crosscheck.py > cn_us_crosscheck_log.txt
python3 cn_test.py | tee cn_test_log.txt
python3 cn_number_audit.py > cn_number_audit_log.txt   # independent recomputation of unit conversions (exits 1 on failure)
tail -1 cn_number_audit_log.txt
python3 cn_sm_tables.py
if [ "$FIGS" = "1" ]; then
  python3 cn_figures.py
fi
# compare this run with the submitted release (file hashes, fresh re-solves, saved numbers; needs the full 1000 draws)
if [ "$N" = "1000" ]; then python3 cn_release_check.py | tee cn_release_check_log.txt; fi
echo "Done: CN v1.6.2 model run, tests and figures in $(pwd)"
