import test from 'node:test';
import assert from 'node:assert/strict';
import { preparePlotData } from '../src/lib/plotRendering.ts';

test('no-WebGL fallback preserves every coordinate, label and style without mutating input', () => {
  const trace = Object.freeze({ type: 'scattergl', x: [0, 1, 2], y: [2, -3, 4], mode: 'lines+markers', name: 'Position (m)', line: { dash: 'dash' }, xaxis: 'x2', yaxis: 'y2' });
  const data = [trace, { type: 'heatmap', z: [[1, 2]] }, { type: 'scatter3d', x: [1], y: [2], z: [3] }];
  const result = preparePlotData(data, false);
  assert.deepEqual(result[0], { ...trace, type: 'scatter' });
  assert.equal(result[0].x, trace.x);
  assert.equal(result[0].y, trace.y);
  assert.equal(trace.type, 'scattergl');
  assert.equal(result[1], data[1]);
  assert.equal(result[2], data[2]); // Never silently flatten a 3D trace.
  assert.deepEqual(preparePlotData(data, true), data);
});
