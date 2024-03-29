import re
from pathlib import Path
from src.dtos.movie import Movie
from src.dtos.preset import Preset


class FileMovieConverter:
    RE_YEAR_PATTERN = r"\b\d{4}\b"
    RE_QUALITY_PATTERN = r"(\b\d+p)"
    RE_TITLE_PATTERN = r"^([^0-9]+)(?=\.)\b"
    UNKNOWN_YEAR = "Unknown Year"
    UNKNOWN_QUALITY = "Unknown Quality"
    UNKNOWN_TITLE = "Unknown Title"

    def __init__(self, preset: Preset, candidates: list[Path]):
        self.preset = preset
        self.candidates = candidates

    def get(self) -> list[Movie]:
        movies = []

        for candidate in self.candidates:
            year: str = self.__extract_info(self.RE_YEAR_PATTERN, candidate.name)
            quality: str = self.__extract_info(self.RE_QUALITY_PATTERN, candidate.name)
            title: str = self.__extract_info(self.RE_TITLE_PATTERN, candidate.name)

            if quality and int(quality[:-1]) < self.preset.picture_height:
                final_quality = quality
            else:
                final_quality = f"{self.preset.picture_height}p"

            movies.append(
                Movie(
                    title=title if title else self.UNKNOWN_TITLE,
                    year=year if year else self.UNKNOWN_YEAR,
                    quality=quality if quality else self.UNKNOWN_QUALITY,
                    full_path=candidate,
                    final_quality=final_quality,
                )
            )

        return movies

    def __extract_info(self, regex_pattern: str, filename: str) -> str | None:
        if match := re.search(re.compile(regex_pattern), filename):
            return match.group(0)
