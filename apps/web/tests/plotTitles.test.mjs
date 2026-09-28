import test from 'node:test';
import assert from 'node:assert/strict';
import { normalizePlotTitles } from '../src/lib/plotTitles.ts';

test('portable chart, secondary axis, scene and colorbar titles survive Plotly 3', () => {
  const original = { title: 'Spectrum', xaxis: { title: 'Frequency (Hz)' },
    yaxis2: { title: { text: 'Phase (rad)', font: { size: 12 } } },
    scene: { zaxis: { title: 'Range (m)' } }, marker: { colorbar: { title: 'Power (dB)' } },
    x: [1, 2], z: [[1, 2], [3, 4]] };
  const result = normalizePlotTitles(original);
  assert.deepEqual(result.xaxis.title, { text: 'Frequency (Hz)' });
  assert.deepEqual(result.title, { text: 'Spectrum' });
  assert.deepEqual(result.yaxis2.title, original.yaxis2.title);
  assert.deepEqual(result.scene.zaxis.title, { text: 'Range (m)' });
  assert.deepEqual(result.marker.colorbar.title, { text: 'Power (dB)' });
  assert.equal(original.xaxis.title, 'Frequency (Hz)');
  assert.equal(result.x, original.x);
  assert.equal(result.z, original.z);
});
