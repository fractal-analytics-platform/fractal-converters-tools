"""Tools to initialize a conversion tasks."""

import pickle
from uuid import uuid4

from fractal_converters_tools.task_common_models import (
    AdvancedComputeOptions,
    ConvertParallelInitArgs,
)
from fractal_converters_tools.tiled_image import TiledImage


def build_parallelization_list(
    zarr_dir: str,
    tiled_images: list[TiledImage],
    advanced_compute_options: AdvancedComputeOptions,
    tmp_dir_name: str | None = None,
) -> list[dict]:
    """Build a list of dictionaries to parallelize the conversion.

    Args:
        zarr_dir (str): The path to the zarr directory.
        tiled_images (list[TiledImage]): A list of tiled images objects to convert.
        advanced_compute_options (AdvancedComputeOptions): The advanced compute options.
        tmp_dir_name (str, optional): The name of the temporary directory to store the
            pickled tiled images.
    """
    parallelization_list = []

    tmp_dir_name = tmp_dir_name if tmp_dir_name else "_tmp_coverter_dir"
    pickle_dir = zarr_dir / tmp_dir_name
    pickle_dir.mkdir(parents=True, exist_ok=True)

    for tile in tiled_images:
        tile_pickle_path = pickle_dir / f"{uuid4()}.pkl"
        with open(tile_pickle_path, "wb") as f:
            pickle.dump(tile, f)
        parallelization_list.append(
            {
                "zarr_url": str(zarr_dir),
                "init_args": ConvertParallelInitArgs(
                    tiled_image_pickled_path=str(tile_pickle_path),
                    advanced_compute_options=advanced_compute_options,
                ).model_dump(),
            }
        )
    return parallelization_list
