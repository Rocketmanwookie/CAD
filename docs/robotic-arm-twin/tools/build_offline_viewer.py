"""Embed the generated mesh for local viewing without HTTP or internet."""
from pathlib import Path

root=Path(__file__).resolve().parents[1]
p=root/'web'/'cad.html';s=p.read_text();mesh=(p.parent/'cad_mesh.json').read_text()
old="const res=await fetch('/cad_mesh.json');if(!res.ok)throw Error('Mesh missing: run tools/export_view_mesh.py with FreeCAD Python.');const mesh=await res.json();"
assert old in s,'Viewer fetch expression changed: update build script'
s=s.replace(old,"const mesh=JSON.parse(document.querySelector('#cad-data').textContent);")
s=s.replace('<script>','<script id="cad-data" type="application/json">'+mesh+'</script>\n<script>',1)
s=s.replace('href="/"','href="../README.md"').replace('Telemetry teaching lab</a>','Package instructions</a>')
(p.parent/'cad-standalone.html').write_text(s)
print('Wrote web/cad-standalone.html (manufacturer geometry; local use)')
