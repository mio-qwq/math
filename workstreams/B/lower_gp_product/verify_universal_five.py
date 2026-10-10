"""One-command full certificate replay, all candidate set sizes1..4."""
from pathlib import Path
import subprocess,sys,json
root=Path(__file__).resolve().parent
expected={1:(1,1),2:(2,2),3:(8,14),4:(106,2381)}
for k in range(1,5):
 r=subprocess.run([sys.executable,str(root/'verify_arbitrary_four.py'),str(k)],capture_output=True,text=True,check=True)
 data=json.loads(r.stdout);assert data['status']=='PASS' and data['selected_size']==k
 assert (data['landmark_models'],data['gp_product_models'])==expected[k]
 print(json.dumps(data,sort_keys=True),flush=True)
print('PASS: universal lower-GP Cartesian-product bound min(5, factor parameters); independent review pending.')
