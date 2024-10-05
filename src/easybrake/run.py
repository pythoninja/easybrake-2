import sys
from pathlib import Path

from loguru import logger

from easybrake.resolver import DirectoryResolver
from easybrake.converters.to_movie import FileMovieConverter
from easybrake.converters.to_preset import PresetConverter
from easybrake.finder import VideoFinder
from easybrake.generator import CommandGenerator
from easybrake.utils.named_type import Directories, Commands, Movies


def runner(input_dir: Path, output_dir: Path, preset_location: str) -> None:
    resolver = DirectoryResolver()
    target_dir = resolver.resolve(output_dir)

    logger.info("Easybrake started")
    logger.info("Preset file location: {}", preset_location)
    logger.info("Input directory: {}", input_dir)
    logger.info("Output directory: {}", output_dir)

    finder = VideoFinder(input_dir=input_dir)
    video_files: list[Path] = finder.find()

    if not video_files:
        logger.error(f"No video files found at selected directory: {input_dir}")
        sys.exit(1)

    preset_converter = PresetConverter(preset_location=preset_location)
    preset = preset_converter.get_preset()

    logger.info("Preset name: {}", preset.name)
    logger.info(
        "Preset parameters: picture_height={}, picture_width={}, upscale_enabled={} ",
        preset.picture_height,
        preset.picture_width,
        preset.upscale_enabled,
    )

    movie_converter = FileMovieConverter(preset=preset, candidates=video_files)
    movies: Movies = movie_converter.get_movies()

    command_generator = CommandGenerator(preset=preset, movies=movies, output_dir=target_dir)
    commands: Commands
    dirs: Directories
    commands, dirs = command_generator.get()

    resolver.create_dirs(dirs)

    print("\n# Generated hanbrake commands, just paste it to the bash script, check and run\n")
    print(*commands, sep="\n\n")
    print("# Paste the code above this line \n")

    logger.info("Easybrake finished")


if __name__ == "__main__":
    from logger import init_logger

    init_logger()

    _preset_filename = "preset-example.json"
    _base_path = Path(__file__).resolve().parent.parent.parent
    _preset_location: str = str(_base_path / "example" / "presets" / _preset_filename)
    _input_dir = _base_path / "example" / "videos" / "process"
    _output_dir = _base_path / "example" / "videos" / "done"

    runner(_input_dir, _output_dir, _preset_location)
