import json
import sys
import tempfile
from pathlib import Path

from loguru import logger

from easybrake.models.preset import Preset
from easybrake.utils.httpclient import HttpClient
from easybrake.utils.url import URLUtils
from easybrake.enums.location import LocationType
from easybrake.utils.named_type import PresetJSON, PresetProperyValues


class PresetConverter:
    def __init__(self, preset_location: str):
        self.full_preset_path = None
        self.preset_location = preset_location
        self.preset_json: PresetJSON | None = self.__load_preset()

    def __load_preset(self) -> PresetJSON:
        location_type = URLUtils.get_location_type(self.preset_location)

        match location_type:
            case LocationType.LOCAL:
                return self.__load_from_disk()
            case LocationType.URL:
                return self.__load_from_url()

    def __load_from_disk(self) -> PresetJSON:
        logger.info("Preset is on a local disk: {}", self.preset_location)
        logger.info("Reading it...")
        self.full_preset_path = Path(self.preset_location)

        return self.__read_json()

    def __load_from_url(self) -> PresetJSON:
        logger.info("Preset is an url: {}", self.preset_location)
        logger.info("Downloading it...")
        client = HttpClient()
        response = client.get(self.preset_location)

        if client.is_error():
            logger.error("Error downloading preset: {}", response.status_code)
            sys.exit(1)

        temp_file = self.save_temp_preset(response.text)
        self.full_preset_path = temp_file

        return self.__read_json()

    def __read_json(self) -> PresetJSON:
        try:
            with self.full_preset_path.open(encoding="UTF-8") as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError) as e:
            self.__handle_json_error(e)

    def __handle_json_error(self, error: FileNotFoundError | json.JSONDecodeError) -> None:
        match error:
            case FileNotFoundError():
                logger.error(f"File {self.preset_location} does not exist.")
            case json.JSONDecodeError():
                logger.error(f"File {self.preset_location} is not a valid JSON.")

        sys.exit(1)

    def __get_preset_property(self, property_name: str) -> PresetProperyValues:
        try:
            return self.preset_json["PresetList"][0][property_name]
        except (KeyError, TypeError):
            logger.error("Invalid JSON structure: Missing {} key.", property_name)
            sys.exit(1)

    def get_preset(self) -> Preset:
        return Preset(
            name=self.__get_preset_property("PresetName"),
            picture_width=self.__get_preset_property("PictureWidth"),
            picture_height=self.__get_preset_property("PictureHeight"),
            path=self.full_preset_path,
            upscale_enabled=self.__get_preset_property("PictureAllowUpscaling"),
        )

    def save_temp_preset(self, content: str) -> Path:
        temp_dir = tempfile.mkdtemp(prefix="preset_")
        temp_file = Path(temp_dir).joinpath("preset.json")
        logger.info("Saving preset to a temp file: {}", temp_file)

        with temp_file.open("w", encoding="UTF-8") as f:
            f.write(content)

        return temp_file
