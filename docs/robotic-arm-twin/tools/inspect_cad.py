"""Run with FreeCAD's Python, with its usr/lib on PYTHONPATH. No source edits."""
import argparse
import hashlib
import json
import re
from pathlib import Path


def inventory(source):
    rows = []
    for p in sorted(source.iterdir()):
        if p.is_file():
            rows.append(dict(name=p.name, bytes=p.stat().st_size,
                             sha256=hashlib.sha256(p.read_bytes()).hexdigest()))
    return rows


def inspect(source, output, step_name):
    import FreeCAD as App
    import Import
    source, output = Path(source), Path(output)
    output.mkdir(parents=True, exist_ok=True)
    step = source / step_name
    text = step.read_text(errors='replace')
    report = dict(source=str(source), source_rights='User-supplied; redistribution unverified',
                  freecad_version=App.Version(), files=inventory(source),
                  step_header=text.split('ENDSEC;')[0],
                  step_products=re.findall(r"PRODUCT\s*\(\s*'([^']*)'", text),
                  declared_mm=bool(re.search(r'SI_UNIT\s*\(\s*\.MILLI\.\s*,\s*\.METRE\.', text)),
                  objects=[])
    doc = App.newDocument('RobotInspection')
    Import.insert(str(step), doc.Name)
    doc.recompute()
    for obj in doc.Objects:
        if not hasattr(obj, 'Shape') or obj.Shape.isNull():
            continue
        s = obj.Shape
        if not s.Solids:
            continue
        b = s.BoundBox
        volume = sum(solid.Volume for solid in s.Solids)
        center = sum((solid.CenterOfMass * solid.Volume for solid in s.Solids), App.Vector()) / volume if volume else App.Vector()
        report['objects'].append(dict(name=obj.Name, label=obj.Label, type=obj.TypeId,
            solids=len(s.Solids), valid=s.isValid(), volume_mm3=s.Volume,
            area_mm2=s.Area, center_of_volume_mm=list(center),
            bbox_mm=[b.XMin,b.YMin,b.ZMin,b.XMax,b.YMax,b.ZMax],
            placement=str(obj.Placement),
            parents=[x.Name for x in obj.InList], children=[x.Name for x in obj.OutList]))
    # Counts of object solids can double-count compound and child representations.
    report['note'] = ('Geometry only. Object counts may include assembly containers. '
        'Center of volume assumes uniform density; no materials, joint axes, '
        'motor constants, or physical masses are inferred.')
    (output / 'cad_inventory.json').write_text(json.dumps(report, indent=2))
    App.closeDocument(doc.Name)
    print('Wrote', output / 'cad_inventory.json')


if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument('source'); p.add_argument('output')
    p.add_argument('--step', default='IRB6720LPS_240kg-265_OC_00_ASM_CAD.step')
    a = p.parse_args(); inspect(a.source, a.output, a.step)
