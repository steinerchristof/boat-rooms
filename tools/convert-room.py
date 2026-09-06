"""Convert a FlashWorld PLY export to SPZ without permuting splat rotations."""
import argparse
import numpy as np
from plyfile import PlyData
import spz

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('input')
parser.add_argument('output')
args = parser.parse_args()
vertices = PlyData.read(args.input)['vertex'].data

def columns(names):
    return np.column_stack([vertices[name] for name in names]).astype(np.float32)

cloud = spz.GaussianCloud()
features = sorted((n for n in vertices.dtype.names if n.startswith('f_dc_')), key=lambda n: int(n[5:]))
cloud.sh_degree = int(np.sqrt(len(features) // 3)) - 1
cloud.positions = columns(['x', 'y', 'z']).ravel()
cloud.scales = columns([f'scale_{i}' for i in range(3)]).ravel()
# FlashWorld/gsplat stores w,x,y,z; SPZ requires x,y,z,w.
rotations = columns(['rot_1', 'rot_2', 'rot_3', 'rot_0'])
cloud.rotations = rotations.ravel()
cloud.alphas = np.asarray(vertices['opacity'], dtype=np.float32)
cloud.colors = columns(features[:3]).ravel()
cloud.sh = columns(features[3:]).ravel()
spz.save_spz(cloud, spz.PackOptions(), args.output)
restored = spz.load_spz(args.output, spz.UnpackOptions())
actual = np.asarray(restored.rotations).reshape(-1, 4)
expected = rotations / np.linalg.norm(rotations, axis=1, keepdims=True)
actual = actual / np.linalg.norm(actual, axis=1, keepdims=True)
angle = 2 * np.arccos(np.clip(np.abs(np.sum(actual * expected, axis=1)), 0, 1))
assert np.max(angle) < 0.01, f'Rotation round-trip error: {np.max(angle)}'
assert len(restored.positions) == len(cloud.positions)
print(f'Validated {len(vertices):,} splats; maximum rotation error {np.degrees(angle.max()):.4f} degrees')
