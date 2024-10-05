from pathlib import Path

from easybrake.models.movie import MovieType
from easybrake.models.preset import Preset
from easybrake.utils.named_type import CommandsAndDirectories, Commands, Directories, Movies


class CommandGenerator:
    def __init__(self, preset: Preset, movies: Movies, output_dir: Path) -> None:
        self.preset = preset
        self.output_dir = output_dir
        self.movies = movies
        self.additional_params = ["--all-audio", "--markers"]

    def get(self) -> CommandsAndDirectories:
        commands: Commands = []
        dirs: Directories = []

        for movie in self.movies:
            title = movie.title
            year = movie.year
            season = movie.season
            episode = movie.episode
            final_quality = movie.final_quality

            if movie.type == MovieType.SHOW:
                output_file = Path(
                    f"{self.output_dir}/{title}/Season {season[1:]}/{title}.{season}{episode}.{final_quality}.mp4"
                )
            else:
                output_file = Path(
                    f"{self.output_dir}/{title} ({year})/{title} ({year}) [imdbid-] - {final_quality}.mp4"
                )

            template = (
                "# Convert {filename}\n"
                'handbrakecli --preset-import-file "{preset_path}"'
                ' --preset "{preset_name}"'
                ' --input "{input_file}"'
                ' --output "{output_file}"'
                " {params}"
            )
            commands.append(
                template.format(
                    preset_path=self.preset.path,
                    preset_name=self.preset.name,
                    input_file=movie.full_path,
                    output_file=output_file,
                    filename=movie.filename,
                    params=" ".join(self.additional_params),
                )
            )

            dirs.append(output_file.parent)

        return commands, dirs
