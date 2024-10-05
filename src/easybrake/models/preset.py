from dataclasses import dataclass
from pathlib import Path


@dataclass
class Preset:
    name: str
    picture_width: int
    picture_height: int
    path: Path
    upscale_enabled: bool
