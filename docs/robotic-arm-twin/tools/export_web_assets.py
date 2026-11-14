"""Export FreeCAD-derived preview mesh as grouped OBJ/MTL and standard glTF 2 GLB.
Geometry stays in meters in the supplied assembly posture. No joint axes inferred.
Python standard library only. Manufacturer geometry retains its source rights.
"""
import argparse
import json
import math
import struct
from pathlib import Path


def export(source, destination):
    model = json.loads(Path(source).read_text())
    vertices, triangles, groups = model['vertices'], model['triangles'], model['groups']
    if model['units'] != 'm' or not vertices or not triangles:
        raise ValueError('Expected a nonempty mesh in meters')
    if not all(len(v) == 3 and all(math.isfinite(x) for x in v) for v in vertices):
        raise ValueError('Invalid vertices')
    if not all(len(t) == 3 and all(type(i) is int and 0 <= i < len(vertices) for i in t) for t in triangles):
        raise ValueError('Invalid triangle indices')
    cursor = 0
    for g in groups:
        if g['start_triangle'] != cursor or g['count'] <= 0:
            raise ValueError('Expected contiguous component groups')
        cursor += g['count']
    if cursor != len(triangles):
        raise ValueError('Groups must cover all triangles exactly once')
    destination = Path(destination)
    destination.mkdir(parents=True, exist_ok=True)
    stem = 'abb_irb6720'
    palette = [('body', [.87, .88, .84]), ('base', [.34, .43, .52]), ('cable', [.16, .24, .31])]
    def material(name):
        return 2 if 'cable' in name.lower() else 1 if 'base' in name.lower() else 0
    with (destination / (stem + '.mtl')).open('w') as f:
        for name, color in palette:
            f.write(f'newmtl {name}\nKd {color[0]} {color[1]} {color[2]}\n\n')
    with (destination / (stem + '.obj')).open('w') as f:
        f.write('# FreeCAD-derived assembly preview. Units: meters. No kinematics.\n')
        f.write(f'mtllib {stem}.mtl\n')
        for v in vertices:
            f.write('v ' + ' '.join(str(x) for x in v) + '\n')
        for g in groups:
            f.write(f"o {g['name'].replace(' ', '_')}\nusemtl {palette[material(g['name'])][0]}\n")
            for t in triangles[g['start_triangle']:g['start_triangle']+g['count']]:
                f.write('f ' + ' '.join(str(i+1) for i in t) + '\n')
    positions = b''.join(struct.pack('<3f', *v) for v in vertices)
    stored_vertices = list(struct.iter_unpack('<3f', positions))
    indices = b''.join(struct.pack('<3I', *t) for t in triangles)
    binary = positions + indices
    gltf = dict(asset={'version': '2.0', 'generator': 'FreeCAD-derived ABB preview export'},
        scene=0, scenes=[{'nodes': list(range(len(groups)))}], nodes=[], meshes=[],
        materials=[{'name': name, 'pbrMetallicRoughness': {'baseColorFactor': color+[1],
                    'metallicFactor': 0, 'roughnessFactor': .7}, 'doubleSided': True} for name,color in palette],
        buffers=[{'byteLength': len(binary)}],
        bufferViews=[{'buffer': 0, 'byteOffset': 0, 'byteLength': len(positions), 'target': 34962},
                     {'buffer': 0, 'byteOffset': len(positions), 'byteLength': len(indices), 'target': 34963}],
        accessors=[{'bufferView': 0, 'componentType': 5126, 'count': len(vertices), 'type': 'VEC3',
                    'min': [min(v[k] for v in stored_vertices) for k in range(3)],
                    'max': [max(v[k] for v in stored_vertices) for k in range(3)]}],
        extras={'source_file': model['source'], 'source_sha256': model['sha256'],
                'status': model['status'], 'units': 'm', 'coordinate_up_axis': '+Y',
                'conversion': 'CAD Z-up -> glTF Y-up by rotating each component -90 degrees about X',
                'geometry_warning': 'Source LINK03 solid is invalid; preview only',
                'rights': 'Manufacturer geometry; redistribution rights not established'})
    # glTF is Y-up. Shared CAD vertices stay Z-up; rotate each component at scene level.
    half = math.sqrt(.5)
    for g in groups:
        index_accessor = len(gltf['accessors'])
        gltf['accessors'].append({'bufferView': 1, 'byteOffset': g['start_triangle']*12,
            'componentType': 5125, 'count': g['count']*3, 'type': 'SCALAR'})
        gltf['nodes'].append({'name': g['name'], 'mesh': len(gltf['meshes']),
                              'rotation': [-half, 0, 0, half]})
        gltf['meshes'].append({'name': g['name'], 'primitives': [{'attributes': {'POSITION': 0},
            'indices': index_accessor, 'material': material(g['name']), 'mode': 4}]})
    encoded = json.dumps(gltf, separators=(',', ':'), allow_nan=False).encode()
    encoded += b' ' * (-len(encoded) % 4)
    binary += b'\0' * (-len(binary) % 4)
    glb = struct.pack('<4sII', b'glTF', 2, 12+8+len(encoded)+8+len(binary))
    glb += struct.pack('<I4s', len(encoded), b'JSON') + encoded
    glb += struct.pack('<I4s', len(binary), b'BIN\0') + binary
    target = destination / (stem + '.glb')
    target.write_bytes(glb)
    print(f'Exported {len(groups)} named components and {len(triangles):,} triangles to {destination}')
    print(f'GLB: {len(glb):,} bytes; preview only, no joint kinematics')
    return target


if __name__ == '__main__':
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('source', type=Path); p.add_argument('destination', type=Path)
    a = p.parse_args(); export(a.source, a.destination)
