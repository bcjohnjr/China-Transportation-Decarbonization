#!/bin/sh
set -eu
cd "$(dirname "$0")"
export OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1
python cn17_validate.py --preflight
python cn17_prepare.py
python cn17_inventory.py
python cn17_evidence.py
python cn17_figures.py
python cn17_validate.py
