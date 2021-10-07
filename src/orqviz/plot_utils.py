import warnings
from typing import Optional, Tuple

import matplotlib
import matplotlib.pyplot as plt
import matplotlib.ticker as tck
import numpy as np


def normalize_color_and_colorbar(
    fig: plt.Figure,
    ax: plt.Axes,
    min_val: float = 0.0,
    max_val: float = 1.0,
    cmap: str = "viridis",
    image_index: int = 0,
):
    """Function to adjust the color and colorbar of a matplotlib plot.

    Args:
        fig: Matplotlib figure in which the plot is performed.
        ax: Matplotlib axis in which the plot is performed.
        min_val: Minimum values of the image and colorbar range. Defaults to 0.0.
        max_val: Maximum values of the image and colorbar range. Defaults to 1.0.
        cmap: Matplotlib colormap for the plot. Defaults to "viridis".
        image_index: Position index for the image in the Matplotlib axis.
            Defaults to 0.

    """
    try:
        image = ax.collections[image_index]
    except (AttributeError, IndexError):
        try:
            image = ax.images[image_index]
        except (AttributeError, IndexError) as e:
            raise e(
                "Provided ax does not contain an image in ax.images or ax.collections"
            )

    image.colorbar.remove()
    image.set_clim(vmin=min_val, vmax=max_val)
    image.set_cmap(cmap)
    fig.colorbar(image, ax=ax)


def get_colorbar_from_ax(
    ax: plt.Axes,
    image_index: Optional[int] = None,
):
    """Helper function to extract the colorbar of a previously created plot.

    Args:
        ax: Matplotlib axis in which the colorbar was created.
        image_index: Position index for the image in the Matplotlib axis.
            If None, will return the first colorbar that is found. Defaults to None.

    """
    if image_index is None:

        len_collections = len(ax.collections)
        len_images = len(ax.images)

        if len_collections > 0:
            for ii in range(len_collections):
                image = ax.collections[ii]
                if hasattr(image, "colorbar"):
                    return image.colorbar

        elif len_images > 0:
            for ii in range(len_images):
                image = ax.images[ii]
                if hasattr(image, "colorbar"):
                    return image.colorbar

        raise AttributeError(
            "Provided ax does not contain an image with a colorbar in ax.images"
            " or ax.collections"
        )

    else:
        try:
            image = ax.collections[image_index]
            return image.colorbar
        except (AttributeError, IndexError):
            try:
                image = ax.images[image_index]
                return image.colorbar
            except (AttributeError, IndexError) as e:
                raise e(
                    "Provided ax does not contain an image in ax.images"
                    " or ax.collections"
                )


def set_ticks_to_multiples_of_pi(ax: plt.Axes, base=np.pi / 2):
    """Helper function to set the ticks of matplotlib axes
    to multiples of pi with pi symbols."""
    ax.xaxis.set_major_formatter(
        tck.FuncFormatter(
            lambda val, pos: "{:.2f}$\pi$".format(val / np.pi)  # noqa: W605
            if val != 0
            else "0"
        )
    )
    ax.xaxis.set_major_locator(tck.MultipleLocator(base=base))

    ax.yaxis.set_major_formatter(
        tck.FuncFormatter(
            lambda val, pos: "{:.2f}$\pi$".format(val / np.pi)  # noqa: W605
            if val != 0
            else "0"
        )
    )
    ax.yaxis.set_major_locator(tck.MultipleLocator(base=base))


def _check_and_create_fig_ax(
    fig: Optional[plt.Figure] = None,
    ax: Optional[plt.Axes] = None,
) -> Tuple[plt.Figure, plt.Axes]:

    if fig is None and ax is None:
        fig = plt.gcf()
        ax = fig.gca()

    elif fig is not None and ax is None:
        ax = fig.gca()

    return fig, ax


def _check_and_create_3D_ax(
    ax: Optional[plt.Axes] = None,
) -> plt.Axes:
    if ax is None:
        fig = matplotlib.pyplot.figure()
        ax = fig.add_subplot(projection="3d")
    elif ax.name != "3d":
        warnings.warn(
            "The matplotlib axis you provided is not a 3d axis. "
            "Your axis is overridden with a new axis."
        )
        warnings.warn("You can create a 3d axis with fig.add_subplot(projection='3d')")
        fig = matplotlib.pyplot.figure()
        ax = fig.add_subplot(projection="3d")

    return ax
