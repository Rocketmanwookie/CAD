"""Offline scientific plotting of the derived CAD mesh; requires numpy/matplotlib."""
import json
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import numpy as np

root=Path(__file__).resolve().parents[1]
m=json.loads((root/'web'/'cad_mesh.json').read_text());v=np.array(m['vertices']);t=np.array(m['triangles'])
tri=v[t];cross=np.cross(tri[:,1]-tri[:,0],tri[:,2]-tri[:,0]);norm=np.linalg.norm(cross,axis=1)
n=cross/np.maximum(norm[:,None],1e-20);sun=np.array([.4,-.6,.8]);sun/=np.linalg.norm(sun)
light=.3+.7*np.abs(n@sun);colors=np.tile([.84,.87,.88],(len(t),1))
for g in m['groups']:
 a=g['start_triangle'];b=a+g['count'];name=g['name'].lower()
 if 'cable' in name:colors[a:b]=[.18,.25,.30]
 elif 'base' in name:colors[a:b]=[.32,.43,.52]
colors*=light[:,None]
fig=plt.figure(figsize=(10,10),facecolor='#132337');ax=fig.add_subplot(projection='3d',facecolor='#132337')
ax.add_collection3d(Poly3DCollection(tri,facecolors=colors,edgecolors='none',rasterized=True))
lo=v.min(axis=0);hi=v.max(axis=0);mid=(lo+hi)/2;span=(hi-lo).max()*1.05
for setter,c in zip([ax.set_xlim,ax.set_ylim,ax.set_zlim],mid):setter(c-span/2,c+span/2)
ax.set_box_aspect((1,1,1));ax.view_init(elev=18,azim=-65);ax.set_axis_off()
fig.text(.07,.94,'ABB IRB 6720-240/2.65',color='white',fontsize=23,weight='bold')
fig.text(.07,.90,'Rendered from your supplied STEP assembly',color='#b8d2e8',fontsize=14)
fig.text(.07,.07,'Static CAD preview • workspace envelope excluded\n12 groups • 187,221 triangles • not connected to hardware',color='#b8d2e8',fontsize=12)
fig.savefig(root/'evidence'/'abb-cad-preview.png',dpi=130,facecolor=fig.get_facecolor(),bbox_inches='tight');plt.close(fig)
print('Wrote evidence/abb-cad-preview.png')
