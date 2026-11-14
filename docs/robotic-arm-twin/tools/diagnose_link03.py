"""Diagnose supplied LINK03 using FreeCAD; repair only a transient copy."""
import argparse
import json,hashlib
from pathlib import Path
import FreeCAD,Part
parser=argparse.ArgumentParser(description=__doc__)
parser.add_argument('source',type=Path)
parser.add_argument('output',type=Path)
args=parser.parse_args()
src=args.source
r={'source':str(src),'sha256':hashlib.sha256(src.read_bytes()).hexdigest(),'source_untouched':True,'purpose':'Read-only diagnosis and repair on a transient copy; no production replacement'}
s=Part.read(str(src));r['standalone_valid_before']=s.isValid();r['volume_before_mm3']=s.Volume;r['solids_before']=len(s.Solids)
try:
 s.check(True);r['check_before']='No exception'
except Exception as e:r['check_before']=str(e)
c=s.copy()
try:
 r['fix_return']=c.fix(1e-7,1e-7,1e-3);r['valid_after_fix']=c.isValid();r['volume_after_mm3']=c.Volume;r['solids_after']=len(c.Solids)
 r['disposition']='Repair still invalid' if not r['valid_after_fix'] else 'Geometric candidate only; engineering equivalence still requires review'
except Exception as e:r['fix_error']=str(e)
args.output.write_text(json.dumps(r,indent=2)+'\n')
print(json.dumps(r,indent=2))
