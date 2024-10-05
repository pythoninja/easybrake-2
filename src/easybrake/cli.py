from cyclopts import App

from easybrake.command import handle_process_command
from easybrake.logger import init_logger
from easybrake import __version__, __app_name__

app = App(version=f"{__app_name__} v{__version__}", version_flags=["--version"], help_flags=["--help"])
app.command(handle_process_command, name="process")

init_logger()

if __name__ == "__main__":
    app()
