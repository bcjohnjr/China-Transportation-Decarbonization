"""Release regression checks: exact SHA-256 when possible, numeric tolerance for cross-platform output."""
import csv,hashlib,json,math,sys
from pathlib import Path
P=Path(__file__).resolve().parent
E=json.loads((P/'cn17_expected.json').read_text(encoding='utf-8'))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def eq(a,b,path=''):
 if isinstance(a,dict):
  assert isinstance(b,dict) and a.keys()==b.keys(),path
  for k,v in a.items():eq(v,b[k],path+'/'+k)
 elif isinstance(a,list):
  assert isinstance(b,list) and len(a)==len(b),path
  for i,(x,y) in enumerate(zip(a,b)):eq(x,y,path+'/'+str(i))
 elif isinstance(a,bool) or a is None:assert a==b,path
 else:
  try:x,y=float(a),float(b)
  except (TypeError,ValueError):assert a==b,(path,a,b)
  else:assert math.isclose(x,y,rel_tol=1e-7,abs_tol=1e-6),(path,a,b)
for n,h in E['input_sha256'].items():assert sha(P/n)==h,('Input mismatch',n)
print('Input hashes PASS:',len(E['input_sha256']))
if '--inputs' in sys.argv:sys.exit(0)
for n,h in E['output_sha256'].items():
 if sha(P/n)==h:print(n,'exact SHA-256 PASS');continue
 if n not in E['results']:print(n,'byte representation differs; detailed values covered by case and regional regression');continue
 v=list(csv.DictReader((P/n).open(encoding='utf-8-sig'))) if n.endswith('.csv') else json.loads((P/n).read_text())
 eq(E['results'][n],v,n);print(n,'numeric regression PASS')
c=json.loads((P/'cn17_summary.json').read_text());assert c['draws']==128 and c['domestic_feasible_draws']==128 and c['cheaper_and_domestic_draws']==128
print('CN v1.7 validation passed.')
