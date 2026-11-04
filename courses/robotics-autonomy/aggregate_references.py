"""Independent aggregate references: no production imports or result inputs."""

from __future__ import annotations

import numpy as np
from scipy.optimize import least_squares
from scipy.sparse import lil_matrix


def joint_slam(count: int, noise: float, broken: bool = False):
    """Complex-coordinate residuals with numerical derivatives and TRF/LSMR.

    Production instead uses explicit real Jacobians and Gauss-Newton line search.
    A fixed first pose removes the gauge for this reference; compare free-gauge
    production results after rigid alignment, never their arbitrary absolute frame.
    """
    angles = np.linspace(0, 2 * np.pi, count)
    truth = 3 * np.cos(angles) + 2j * np.sin(angles)
    headings = angles + np.pi / 2
    true_map = np.array([-0.8 + 0.4j, 0.9 - 0.6j, 0.1 + 1.1j])
    k = np.arange(count - 1)
    odom = (truth[1:] - truth[:-1]) * np.exp(-1j * headings[:-1]) + 0.006 * (
        np.sin(k) + 1j * np.cos(1.3 * k)
    )
    turns = np.diff(headings) + 0.0012 * np.sin(0.8 * k)
    observations = np.array(
        [
            [
                (l - truth[i]) * np.exp(-1j * headings[i])
                + 0.004 * (np.sin(0.7 * i + j) + 1j * np.cos(1.1 * i - j))
                for j, l in enumerate(true_map)
            ]
            for i in range(count)
        ]
    )
    initial_poses = np.column_stack(
        (
            truth.real + 0.12 * np.sin(1.7 * angles),
            truth.imag + 0.12 * np.cos(1.3 * angles),
            headings + 0.05 * np.sin(angles),
        )
    )
    initial_map = np.column_stack((true_map.real + 0.16, true_map.imag - 0.12))
    initial = np.r_[initial_poses.ravel(), initial_map.ravel()]
    prior = np.array([truth[0].real, truth[0].imag, headings[0]])

    def residual(x):
        poses = x[: 3 * count].reshape(-1, 3)
        z = poses[:, 0] + 1j * poses[:, 1]
        theta = poses[:, 2]
        maps = x[3 * count :].reshape(-1, 2)
        lm = maps[:, 0] + 1j * maps[:, 1]
        delta = (z[1:] - z[:-1]) * np.exp(-1j * theta[:-1]) - odom
        closing = (z[-1] - z[0]) * np.exp(-1j * theta[0]) - (noise - 0.5j * noise)
        obs = (lm[None, :] - z[:, None]) * np.exp(-1j * theta[:, None]) - observations
        return np.r_[
            (poses[0] - prior) / 0.01,
            np.column_stack(
                (delta.real / 0.03, delta.imag / 0.03, (np.diff(theta) - turns) / 0.015)
            ).ravel(),
            closing.real / max(noise, 0.02),
            closing.imag / max(noise, 0.02),
            (theta[-1] - theta[0] - 2 * np.pi) / 0.02,
            np.stack((obs.real / 0.025, obs.imag / 0.025), axis=-1).ravel(),
        ]

    pattern = lil_matrix((3 + 3 * (count - 1) + 3 + 6 * count, len(initial)))
    pattern[:3, :3] = 1
    row = 3
    for i in range(count - 1):
        pattern[row : row + 3, 3 * i : 3 * i + 6] = 1
        row += 3
    pattern[row : row + 3, :3] = 1
    pattern[row : row + 3, 3 * count - 3 : 3 * count] = 1
    row += 3
    for i in range(count):
        for j in range(3):
            pattern[row : row + 2, 3 * i : 3 * i + 3] = 1
            pattern[row : row + 2, 3 * count + 2 * j : 3 * count + 2 * j + 2] = 1
            row += 2
    solved = least_squares(
        residual,
        initial,
        jac="3-point",
        jac_sparsity=pattern.tocsr(),
        ftol=1e-12,
        xtol=1e-12,
        gtol=1e-10,
        max_nfev=100,
        tr_options={"atol": 1e-13, "btol": 1e-13},
    )
    assert solved.success, solved.message
    return {
        "poses": solved.x[: 3 * count].reshape(count, 3),
        "landmarks": solved.x[3 * count :].reshape(3, 2),
        "cost": float(solved.fun @ solved.fun),
        "free_gauge_requested": broken,
    }
