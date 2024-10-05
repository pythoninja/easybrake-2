from pathlib import Path

import pytest

from easybrake.models.preset import Preset


@pytest.fixture(scope="module")
def preset_fixture():
    return Preset(
        name="Preset - 1080p60 - RF19",
        picture_width=1920,
        picture_height=1080,
        path=Path("/dummy/presets/preset-1080p60-rf19-veryslow_draft-01.json"),
        upscale_enabled=False,
    )
