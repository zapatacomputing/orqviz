import os

import matplotlib.pyplot as plt
import numpy as np
import pytest

from orqviz.hessians import (
    get_Hessian,
    get_Hessian_SPSA_approx,
    perform_1D_hessian_eigenvector_scan,
    plot_1D_hessian_eigenvector_scan_result,
)
from orqviz.io import load_viz_object, save_viz_object


def COST_FUNCTION(params):
    return np.sum(np.sin(params)) + np.sum(params**2)


@pytest.mark.parametrize(
    "params",
    [np.random.rand(8)],
)
def test_get_hessian(params):
    hessian = get_Hessian(params, COST_FUNCTION, gradient_function=None, eps=1e-3)

    assert hasattr(hessian, "eigenvectors")
    assert hasattr(hessian, "eigenvalues")
    assert (
        len(hessian.eigenvalues)
        == len(hessian.eigenvectors)
        == len(hessian.eigenvectors.T)
        == len(params)
    )

    save_viz_object(hessian, "test")
    loaded_hessian = load_viz_object("test")
    os.remove("test")
    np.testing.assert_array_almost_equal(
        loaded_hessian.eigenvalues, hessian.eigenvalues
    )
    np.testing.assert_array_almost_equal(
        loaded_hessian.eigenvectors, hessian.eigenvectors
    )


@pytest.mark.parametrize(
    "params",
    [np.random.rand(8)],
)
def test_get_hessian_SPSA_approx(params):
    hessian = get_Hessian_SPSA_approx(
        params, COST_FUNCTION, gradient_function=None, eps=1e-3, n_reps=20
    )

    assert hasattr(hessian, "eigenvectors")
    assert hasattr(hessian, "eigenvalues")
    assert (
        len(hessian.eigenvalues)
        == len(hessian.eigenvectors)
        == len(hessian.eigenvectors.T)
        == len(params)
    )
    save_viz_object(hessian, "test")
    loaded_hessian = load_viz_object("test")
    os.remove("test")
    np.testing.assert_array_almost_equal(
        loaded_hessian.eigenvalues, hessian.eigenvalues
    )
    np.testing.assert_array_almost_equal(
        loaded_hessian.eigenvectors, hessian.eigenvectors
    )


def test_get_hessian_gives_correct_values():
    params = np.zeros(4)
    eps = 1e-5
    target_matrix = 2*np.eye(4)
    target_eigenvalues = 2*np.ones(4)

    hessian_exact = get_Hessian(params, COST_FUNCTION, gradient_function=None, eps=eps)
    hessian_approx = get_Hessian_SPSA_approx(
        params, COST_FUNCTION, gradient_function=None, eps=eps, n_reps=10000
    )
    precision = int(np.abs(np.log10(eps)))
    
    np.testing.assert_array_almost_equal(hessian_exact.hessian_matrix, target_matrix, precision)
    np.testing.assert_array_almost_equal(hessian_exact.eigenvalues, target_eigenvalues, precision)

    np.testing.assert_array_almost_equal(hessian_approx.hessian_matrix, target_matrix, approx_precision)
    np.testing.assert_array_almost_equal(hessian_approx.eigenvalues, target_eigenvalues, approx_precision)

