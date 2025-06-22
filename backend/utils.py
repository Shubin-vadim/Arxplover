import json
import logging
import re
import sys

import yaml

from backend.core.schemes.config_schemes import ConfigModel


logger = logging.getLogger(__name__)


def load_config_yaml(config_path: str = "./") -> ConfigModel:
    """Load and parse the YAML configuration file.

    Args:
        config_path: Path to the YAML configuration file.

    Returns:
        Parsed configuration as a ConfigModel instance.
    """
    logger.info("Loading YAML configuration from: %s", config_path)
    try:
        with open(config_path, "r", encoding="utf-8") as config_file:
            config = yaml.safe_load(config_file)
            logger.debug("YAML configuration loaded: %s", config)
            return ConfigModel(**config)

    except FileNotFoundError:
        logger.error("YAML file not found at %s", config_path)
        sys.exit(1)
    except yaml.YAMLError as e:
        logger.error("Error parsing YAML file at %s: %s", config_path, e)
        sys.exit(1)


def extract_json_from_string(content: str) -> dict | None:
    """Extract JSON data from a string.

    Args:
        content: The string from which to extract JSON data.

    Returns:
        A dictionary containing the extracted JSON data, or None if no JSON is found.
    """
    logger.info("Extracting JSON from content")
    match = re.search(r"({.*})|(\[.*\])", content, re.DOTALL)
    if match:
        json_str = match.group(0)
        try:
            return json.loads(json_str)
        except json.JSONDecodeError as e:
            logger.error("Error parsing JSON: %s", e)
    else:
        logger.error("JSON not found in the content")
    return None
