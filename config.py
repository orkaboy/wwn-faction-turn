"""Opens the config.yaml file and parses it into a dict."""

import logging

import yaml

try:
    from yaml import CDumper as Dumper, CLoader as Loader
except ImportError:
    from yaml import Dumper, Loader

logger = logging.getLogger(__name__)

CONFIG_FILE_PATH = "config.yaml"


def open_config() -> dict:
    """Open the config file and parse the yaml contents."""
    return open_yaml(CONFIG_FILE_PATH)


def open_yaml(filename: str) -> dict:
    """Open the yaml file and parse its contents."""
    try:
        with open(filename, encoding="utf-8") as yaml_file:
            try:
                return yaml.load(yaml_file, Loader=Loader)
            except Exception:
                logger.error(f"Error: Failed to parse file {filename}")
                logger.exception()
                return {}
    except Exception:
        logger.info(f"Didn't find file {filename}, using default values.")
        return {}


def write_yaml(filename: str, data: dict) -> None:
    """Write dictionary to file."""
    with open(filename, mode="w", encoding="utf-8") as yaml_file:
        try:
            return yaml.dump(data, yaml_file, Dumper=Dumper)
        except Exception:
            logger.error(f"Error: Failed to write to file {filename}")
            logger.exception()
            return {}
