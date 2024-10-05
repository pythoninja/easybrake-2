import re

import pytest

from easybrake.converters.to_movie import FileMovieConverter
from tests.utils.helpers import get_input


@pytest.mark.parametrize("test_input", get_input(_for="year_ok"))
def test_year_parsing_success(preset_fixture, test_input):
    movie_converter = FileMovieConverter(preset_fixture, test_input)
    movies = movie_converter.get_movies()

    assert movies[0].year is not None
    assert movies[0].year is not FileMovieConverter.UNKNOWN_YEAR
    assert re.match(FileMovieConverter.RE_YEAR_PATTERN, movies[0].year)


@pytest.mark.parametrize("test_input", get_input(_for="year_fail"))
def test_year_parsing_unsuccess(preset_fixture, test_input):
    movie_converter = FileMovieConverter(preset_fixture, test_input)
    movies = movie_converter.get_movies()

    assert movies[0].year is not None
    assert movies[0].year == FileMovieConverter.UNKNOWN_YEAR


@pytest.mark.parametrize("test_input", get_input(_for="quality_ok"))
def test_quality_parsing_success(preset_fixture, test_input):
    movie_converter = FileMovieConverter(preset_fixture, test_input)
    movies = movie_converter.get_movies()

    assert movies[0].quality is not None
    assert movies[0].quality is not FileMovieConverter.UNKNOWN_QUALITY


@pytest.mark.parametrize("test_input", get_input(_for="quality_fail"))
def test_quality_parsing_unsuccess(preset_fixture, test_input):
    movie_converter = FileMovieConverter(preset_fixture, test_input)
    movies = movie_converter.get_movies()

    assert movies[0].quality is not None
    assert movies[0].quality is FileMovieConverter.UNKNOWN_QUALITY


# TODO: fix regex or change detection method
@pytest.mark.xfail()
@pytest.mark.parametrize("test_input", get_input(_for="title_expected_fail"))
def test_title_expected_fail(preset_fixture, test_input):
    movie_converter = FileMovieConverter(preset_fixture, test_input)
    movies = movie_converter.get_movies()

    assert movies[0].title is not None
    assert movies[0].title != FileMovieConverter.UNKNOWN_TITLE
    assert movies[0].title == "Film"
