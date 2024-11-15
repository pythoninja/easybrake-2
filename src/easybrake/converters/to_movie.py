import re
from pathlib import Path

from loguru import logger

from easybrake.models.movie import Movie, MediaType
from easybrake.models.preset import Preset
from easybrake.utils.named_type import Movies, ShowSeasonEpisodeOrNone


class FileMovieConverter:
    RE_YEAR_PATTERN = r"\b\d{4}\b"
    RE_QUALITY_PATTERN = r"(\b\d+p)"
    RE_TITLE_PATTERN = r"^([^0-9]+)(?=\.)\b"
    RE_SHOW_PATTERN = r"\b([sS]\d{2})([eE]\d{2})\b"
    UNKNOWN_YEAR = "Unknown Year"
    UNKNOWN_QUALITY = "Unknown Quality"
    UNKNOWN_TITLE = "Unknown Title"
    REPLACEABLE_SYMBOLS = (".", ",", "-", "_")

    def __init__(self, preset: Preset, candidates: list[Path]):
        self.preset = preset
        self.candidates = candidates

    def get_movies(self) -> Movies:
        movies: Movies = []

        for candidate in self.candidates:
            year: str = self.__extract_info(self.RE_YEAR_PATTERN, candidate.name)
            quality: str = self.__extract_info(self.RE_QUALITY_PATTERN, candidate.name)
            title: str = self.__extract_info(self.RE_TITLE_PATTERN, candidate.name)
            show: str = self.__extract_info(self.RE_SHOW_PATTERN, candidate.name)
            season, episode = self.__extract_show_info(self.RE_SHOW_PATTERN, candidate.name)

            logger.info("Extracting info from file: {}", candidate.name)

            final_quality = self.__calculate_final_quality(quality)
            final_title = self.__normalize_title(title) if title else self.UNKNOWN_TITLE
            movie_type = MediaType.SHOW if show else MediaType.FILM

            movies.append(
                Movie(
                    title=final_title,
                    year=year if year else self.UNKNOWN_YEAR,
                    quality=quality if quality else self.UNKNOWN_QUALITY,
                    full_path=candidate,
                    filename=candidate.name,
                    final_quality=final_quality,
                    type=movie_type,
                    season=season if season else None,
                    episode=episode if episode else None,
                )
            )

            logger.info(
                "Extracted values: title={}, year={}, final_quality={}, type={}, season={}, episode={}",
                final_title,
                year,
                final_quality,
                movie_type,
                season,
                episode,
            )

        return movies

    def __extract_info(self, regex_pattern: str, filename: str) -> str | None:
        if match := re.search(re.compile(regex_pattern), filename):
            return match.group(0)

    def __extract_show_info(self, regex_pattern: str, filename: str) -> ShowSeasonEpisodeOrNone:
        if match := re.search(re.compile(regex_pattern), filename):
            return match.group(1), match.group(2)
        return None, None

    def __normalize_title(self, title: str) -> str:
        for symbol in FileMovieConverter.REPLACEABLE_SYMBOLS:
            if symbol in title:
                title = title.replace(symbol, " ")

        return title

    def __calculate_final_quality(self, quality: str) -> str:
        if quality:
            if int(quality[:-1]) < self.preset.picture_height:
                return quality
            else:
                return f"{self.preset.picture_height}p"
        else:
            return self.UNKNOWN_QUALITY
