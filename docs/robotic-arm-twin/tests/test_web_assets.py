import importlib.util
import json
from pathlib import Path
import struct
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('export_web_assets', ROOT/'tools/export_web_assets.py')
exporter = importlib.util.module_from_spec(spec)
spec.loader.exec_module(exporter)


class WebAssetsTests(unittest.TestCase):
    def test_named_components_and_binary_geometry_round_trip(self):
        model = dict(units='m', source='example.step', sha256='example', status='example',
            vertices=[[0,0,0],[1,0,0],[0,1,0],[0,0,1]], triangles=[[0,1,2],[0,2,3]],
            groups=[dict(name='body', start_triangle=0,count=1),dict(name='cable',start_triangle=1,count=1)])
        with tempfile.TemporaryDirectory() as tmp:
            source=Path(tmp)/'mesh.json';source.write_text(json.dumps(model))
            target=exporter.export(source,Path(tmp)/'out');data=target.read_bytes()
            magic,version,total=struct.unpack_from('<4sII',data)
            self.assertEqual((magic,version,total),(b'glTF',2,len(data)))
            size,kind=struct.unpack_from('<I4s',data,12);self.assertEqual(kind,b'JSON')
            gltf=json.loads(data[20:20+size]);binary_start=20+size
            bin_size,kind=struct.unpack_from('<I4s',data,binary_start);self.assertEqual(kind,b'BIN\0')
            binary=data[binary_start+8:];self.assertEqual(bin_size,len(binary))
            self.assertEqual([n['name'] for n in gltf['nodes']],['body','cable'])
            for node in gltf['nodes']:
                self.assertAlmostEqual(sum(x*x for x in node['rotation']),1)
            self.assertEqual(list(struct.iter_unpack('<3f',binary[:48])),[tuple(v) for v in model['vertices']])
            self.assertEqual(list(struct.iter_unpack('<3I',binary[48:])),[(0,1,2),(0,2,3)])
            self.assertEqual(gltf['accessors'][2]['byteOffset'],12)
            self.assertEqual(gltf['meshes'][1]['primitives'][0]['material'],2)
            obj=target.with_suffix('.obj').read_text()
            self.assertIn('o body\n',obj);self.assertIn('o cable\n',obj)
            self.assertIn('f 1 2 3\n',obj);self.assertIn('f 1 3 4\n',obj)

    def test_invalid_index_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            source=Path(tmp)/'mesh.json';source.write_text(json.dumps(dict(units='m',
                vertices=[[0,0,0]],triangles=[[0,1,2]],groups=[])))
            with self.assertRaisesRegex(ValueError,'triangle indices'):
                exporter.export(source,Path(tmp)/'out')


if __name__ == '__main__':unittest.main()
