"""A module to represent an acquisition."""

from typing import Protocol

from ngio.ngff_meta.fractal_image_meta import PixelSize

from fractal_converters_tools.tile import Tile


class PathBuilder(Protocol):
    """A protocol to build paths."""

    @property
    def path(self) -> str:
        """Return the path the relative path for the tiled image."""
        ...


def _zarrify_path(path: str) -> str:
    """Return the zarrified path."""
    if not path.endswith(".zarr"):
        return f"{path}.zarr"
    return path


class SimplePathBuilder:
    """A class to build simple paths."""

    def __init__(self, path: str):
        """Initialize the path builder."""
        self._path = path

    @property
    def path(self) -> str:
        """Return the zarr relative path."""
        return _zarrify_path(self._path)


class PathBuilderPlate:
    """A class to build paths for a standard plate."""

    def __init__(self, plate: str, row: str, column: int, acquisition_id: int):
        """Initialize the path builder."""
        self._plate = plate
        self._row = row
        self._column = column
        self._acquisition_id = acquisition_id

    @property
    def plate(self) -> str:
        """Return the plate."""
        return self._plate

    @property
    def row(self) -> str:
        """Return the row."""
        return self._row

    @property
    def column(self) -> int:
        """Return the column."""
        return self._column

    @property
    def acquisition_id(self) -> int:
        """Return the acquisition ID."""
        return self._acquisition_id

    @property
    def plate_path(self) -> str:
        """Return the plate path."""
        return _zarrify_path(self.plate)

    @property
    def well_path(self) -> str:
        """Return the well path."""
        return f"{self.plate_path}/{self.row}/{self.column}"

    @property
    def path(self) -> str:
        """Return the zarr relative path."""
        return f"{self.well_path}/{self.acquisition_id}"


class TiledImage:
    """A class to represent an acquisition."""

    def __init__(
        self,
        name: str,
        path_builder: PathBuilder,
        num_levels: int = 5,
    ):
        """Initialize the acquisition."""
        self._name = name
        self._path_builder = path_builder
        self.tiles = []
        # User input will override the values from the tiles
        self.num_levels = num_levels

    @property
    def tiles(self) -> list[Tile]:
        """Return the tiles."""
        return self._tiles

    def add_tile(self, Tile):
        """Add a tile to the acquisition."""
        self._tiles.append(Tile)

    @property
    def path_builder(self) -> PathBuilder:
        """Return the path builder."""
        return self._path_builder

    @property
    def path(self) -> str:
        """Return the zarr relative path."""
        return self.path_builder.path

    @property
    def channel_names(self) -> list[str] | None:
        """Return the channel names."""
        if len(self.tiles) == 0:
            return None
        return self.tiles[0].channel_names

    @property
    def wavelength_ids(self) -> list[int] | None:
        """Return the wavelength ids."""
        if len(self.tiles) == 0:
            return None
        return self.tiles[0].wavelength_ids

    @property
    def pixel_size(self) -> PixelSize | None:
        """Return the pixel size."""
        if len(self.tiles) == 0:
            return None
        return self.tiles[0].pixel_size
