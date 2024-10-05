from typing import AnyStr
from urllib.parse import urlparse

from loguru import logger

from easybrake.enums.location import LocationType


class URLUtils:
    @staticmethod
    def get_location_type(url: str) -> LocationType:
        scheme = URLUtils.extract_scheme(url)
        logger.info("Scheme type: {}", scheme or "local")

        match scheme:
            case "https" | "http":
                return LocationType.URL
            case _:
                return LocationType.LOCAL

    @staticmethod
    def extract_scheme(url: str) -> AnyStr:
        return urlparse(url).scheme
