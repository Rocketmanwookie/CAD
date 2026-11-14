"""Generate a clearly marked teaching URDF or a measured visual model.
All lengths SI meters. XYZ and RPY refer to parent->joint zero transform.
Visual boxes are placeholders; use the guide to substitute measured local meshes.
"""
import argparse
import json
import math
from pathlib import Path
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]


def vector(v, n):
    return isinstance(v,list) and len(v)==n and all(type(x) in (int,float) and math.isfinite(x) for x in v)


def build(model, demo=False):
    if model.get('status') != 'measured' and not demo:
        raise ValueError('Unmeasured model: fill measured template or explicitly use --demo')
    joints = model.get('joints',[])
    if len(joints)!=6:
        raise ValueError('Six measured arm joints required')
    robot=ET.Element('robot',name='EXAMPLE_arm' if demo else 'measured_arm')
    ET.SubElement(robot,'link',name='world')
    base=ET.SubElement(robot,'link',name='base_link')
    fixed=ET.SubElement(robot,'joint',name='world_to_base',type='fixed')
    ET.SubElement(fixed,'parent',link='world'); ET.SubElement(fixed,'child',link='base_link')
    parent='base_link'
    for i,j in enumerate(joints,1):
        for key in ('xyz_m','rpy_rad','axis'):
            if not vector(j.get(key),3): raise ValueError(f'joint_{i}: missing {key}')
        if abs(sum(x*x for x in j['axis'])-1)>1e-6: raise ValueError('Axis must be unit length')
        if not vector(j.get('limits'),4): raise ValueError('Need lower,upper,effort,velocity')
        lo,hi,eff,vel=j['limits']
        if not lo<hi or eff<=0 or vel<=0: raise ValueError('Invalid limits')
        child=f'link_{i}'; link=ET.SubElement(robot,'link',name=child)
        vis=ET.SubElement(link,'visual'); geo=ET.SubElement(vis,'geometry')
        ET.SubElement(geo,'box',size='.06 .06 .08')
        joint=ET.SubElement(robot,'joint',name=f'joint_{i}',type='revolute')
        ET.SubElement(joint,'parent',link=parent); ET.SubElement(joint,'child',link=child)
        fmt=lambda x:' '.join(str(a) for a in x)
        ET.SubElement(joint,'origin',xyz=fmt(j['xyz_m']),rpy=fmt(j['rpy_rad']))
        ET.SubElement(joint,'axis',xyz=fmt(j['axis']))
        ET.SubElement(joint,'limit',lower=str(lo),upper=str(hi),effort=str(eff),velocity=str(vel))
        parent=child
    # Deliberately visualization only: no fictional inertia or controllers.
    ET.indent(robot)
    return '<?xml version="1.0"?>\n<!-- VISUALIZATION ONLY: placeholder boxes, no collision or dynamics -->\n'+ET.tostring(robot,encoding='unicode')+'\n'


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--demo',action='store_true'); p.add_argument('--model',type=Path)
    p.add_argument('--output',type=Path,default=Path('/tmp/robot.urdf'))
    a=p.parse_args(); model=a.model or ROOT/'config'/('example_model.json' if a.demo else 'measured_model.template.json')
    try: a.output.write_text(build(json.loads(model.read_text()),a.demo))
    except ValueError as e: p.error(str(e))
    print('Wrote visual model:',a.output)
