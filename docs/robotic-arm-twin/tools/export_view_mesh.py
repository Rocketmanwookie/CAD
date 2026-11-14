"""FreeCAD Python: assembled STEP -> local browser mesh, excluding workspace.
No source edits. Preview meshes are not certified collision/inertia models.
"""
import argparse
import hashlib
import json
from pathlib import Path

if __name__=='__main__':
    import FreeCAD as App
    import Import
    import MeshPart
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('step');p.add_argument('output');a=p.parse_args()
    source=Path(a.step);doc=App.newDocument('Preview');Import.insert(str(source),doc.Name);doc.recompute()
    vertices=[];triangles=[];groups=[]
    for obj in doc.Objects:
        if not hasattr(obj,'Shape') or not obj.Shape.Solids: continue
        if 'working' in obj.Label.lower():continue
        if any(hasattr(c,'Shape') and c.Shape.Solids for c in obj.OutList):continue
        shape=obj.Shape.copy()
        # This import's leaf Shape already includes its object Placement.
        # Account for any parent assembly container placement exactly once.
        if hasattr(obj,'getGlobalPlacement'):
            parent_placement=obj.getGlobalPlacement().multiply(obj.Placement.inverse())
            shape.Placement=parent_placement.multiply(shape.Placement)
        mesh=MeshPart.meshFromShape(Shape=shape,LinearDeflection=3.0,AngularDeflection=.45,Relative=False)
        pts,faces=mesh.Topology;offset=len(vertices);start=len(triangles)
        vertices.extend([[round(float(x)*.001,6) for x in v] for v in pts])
        triangles.extend([[offset+i for i in t] for t in faces])
        groups.append(dict(name=obj.Label,start_triangle=start,count=len(faces)))
    out=dict(source=source.name,sha256=hashlib.sha256(source.read_bytes()).hexdigest(),
        units='m',status='CAD preview; workspace excluded; uncalibrated; no telemetry binding',
        vertices=vertices,triangles=triangles,groups=groups)
    Path(a.output).write_text(json.dumps(out,separators=(',',':')))
    App.closeDocument(doc.Name)
    print('Vertices:',len(vertices),'Triangles:',len(triangles),'Groups:',len(groups))
