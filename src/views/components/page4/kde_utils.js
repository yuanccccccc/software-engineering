import { mean } from 'd3-array';

export function epanechnikovKernel(bandwidth) {
  return function (u) {
    u /= bandwidth;
    return Math.abs(u) <= 1 ? 0.75 * (1 - u * u) / bandwidth : 0;
  };
}

export function kernelDensityEstimator(kernel, sample) {
  return function (x) {
    return x.map(xVal => {
      return [xVal, mean(sample.map(v => kernel(xVal - v)))];
    });
  };
}
