"""Fail-closed CN v1.7 regression validation (validation-only revision).
Preflight checks the complete published delta plus the foundational solver inputs.
Postflight checks every numeric output, all regenerated graphics, and the preserved map.
"""
import argparse
import csv
import hashlib
import json
import math
from pathlib import Path
from PIL import Image

P = Path(__file__).resolve().parent
E = json.loads((P / 'cn17_expected.json').read_text(encoding='utf-8'))


def require(condition, message):
    if not condition:
        raise ValueError(message)


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def eq(expected, actual, path='', csv_values=False):
    """Strict schema/strings/booleans, tolerant finite numbers; recurse through all values."""
    if isinstance(expected, dict):
        require(isinstance(actual, dict) and expected.keys() == actual.keys(), f'{path}: keys differ')
        for k, v in expected.items():
            eq(v, actual[k], f'{path}/{k}', csv_values)
    elif isinstance(expected, list):
        require(isinstance(actual, list) and len(expected) == len(actual), f'{path}: list length/type differs')
        for i, (x, y) in enumerate(zip(expected, actual)):
            eq(x, y, f'{path}/{i}', csv_values)
    elif isinstance(expected, bool) or expected is None:
        require(type(expected) is type(actual) and expected == actual, f'{path}: {expected!r} != {actual!r}')
    elif isinstance(expected, (int, float)) and not isinstance(actual, bool):
        require(isinstance(actual, (int, float)), f'{path}: expected numeric value')
        require(math.isfinite(expected) and math.isfinite(actual) and math.isclose(expected, actual, rel_tol=1e-7, abs_tol=1e-6), f'{path}: {expected!r} != {actual!r}')
    elif csv_values and isinstance(expected, str) and isinstance(actual, str):
        try:
            x, y = float(expected), float(actual)
        except ValueError:
            require(expected == actual, f'{path}: {expected!r} != {actual!r}')
        else:
            require(math.isfinite(x) and math.isfinite(y) and math.isclose(x, y, rel_tol=1e-7, abs_tol=1e-6), f'{path}: {expected!r} != {actual!r}')
    else:
        require(type(expected) is type(actual) and expected == actual, f'{path}: {expected!r} != {actual!r}')


def input_checks():
    for name, digest in E['input_sha256'].items():
        require(sha(P / name) == digest, f'Input mismatch: {name}')
    print('Input hashes PASS:', len(E['input_sha256']))


def preflight():
    with (P / 'CN17_DELTA_SHA256.csv').open(encoding='utf-8-sig', newline='') as f:
        rows = list(csv.DictReader(f))
    names = [r['file'] for r in rows]
    require(len(names) == len(set(names)), 'Duplicate delta manifest entry')
    require(set(names) == set(E['delta_files']), 'Delta manifest inventory differs from expected release')
    for row in rows:
        name = row['file']
        require(Path(name).name == name, f'Non-flat manifest path: {name}')
        require(sha(P / name) == row['sha256'], f'Delta preflight mismatch: {name}')
    print('Whole-delta preflight PASS:', len(rows))
    input_checks()


def numeric_checks():
    require(E['output_sha256'].keys() == E['results'].keys(), 'Expected numerical fallback coverage is incomplete')
    for name, digest in E['output_sha256'].items():
        path = P / name
        if sha(path) == digest:
            print(name, 'exact SHA-256 PASS')
            continue
        if name.endswith('.csv'):
            with path.open(encoding='utf-8-sig', newline='') as f:
                value = list(csv.DictReader(f))
        else:
            value = json.loads(path.read_text(encoding='utf-8'))
        eq(E['results'][name], value, name, csv_values=name.endswith('.csv'))
        print(name, 'complete numerical regression PASS')
    c = json.loads((P / 'cn17_summary.json').read_text(encoding='utf-8'))
    require(c['draws'] == c['domestic_feasible_draws'] == c['cheaper_and_domestic_draws'] == 128, 'Uncertainty counts changed')


def figure_checks():
    for name, reference in E['figures'].items():
        path = P / name
        with Image.open(path) as im:
            require(list(im.size) == reference['size'], f'{name}: image dimensions differ')
            require(im.format == reference['format'], f'{name}: format differs')
            if reference['dpi'] is not None:
                dpi = im.info.get('dpi')
                require(dpi is not None and all(math.isclose(float(a), float(b), abs_tol=0.1) for a,b in zip(dpi, reference['dpi'])), f'{name}: DPI metadata differs')
            pixels = hashlib.sha256(im.convert('RGB').tobytes()).hexdigest()
            require(pixels == reference['rgb_sha256'], f'{name}: regenerated pixels differ; inspect rendering environment')
        if sha(path) == reference['sha256']:
            print(name, 'exact SHA-256 + RGB PASS')
        else:
            print(name, 'RGB, dimensions and DPI PASS (file encoding differs)')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    group = parser.add_mutually_exclusive_group()
    group.add_argument('--preflight', action='store_true')
    group.add_argument('--inputs', action='store_true', help='check foundational inputs only')
    group.add_argument('--outputs-only', action='store_true', help='check published outputs without claiming a fresh run')
    args = parser.parse_args()
    if args.preflight:
        preflight()
    elif args.inputs:
        input_checks()
    else:
        if not args.outputs_only:
            input_checks()
        numeric_checks()
        figure_checks()
        print('CN v1.7 validation passed.' if not args.outputs_only else 'Published numerical and visual regression checks passed (outputs only).')


if __name__ == '__main__':
    main()
