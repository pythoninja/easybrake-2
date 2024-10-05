from pathlib import Path
from typing import Annotated

from cyclopts import Parameter

from easybrake.run import runner

PRESET_LOCATION_ARGUMENT = Annotated[str, Parameter(name="--preset-path")]


def handle_process_command(input_dir: Path, output_dir: Path, preset_location: PRESET_LOCATION_ARGUMENT):
    """
    Process the path and generate easybrake commands
    """

    runner(input_dir, output_dir, preset_location)
