import yaml
import sys
import logging

from backend.core.schemas.config_schemas import ConfigModel

logger = logging.getLogger(__name__)

def load_config_yaml(config_path: str = "./") -> ConfigModel:
    """Load and parse the YAML configuration file.

    Args:
        config_path: Path to the YAML configuration file.

    Returns:
        Parsed configuration as a ConfigModel instance.
    """
    logger.info(f"Loading YAML configuration from: {config_path}")
    try:
        with open(config_path, "r", encoding="utf-8") as config_file:
            config = yaml.safe_load(config_file)
            logger.debug(f"YAML configuration loaded: {config}")
            return ConfigModel(**config)

    except FileNotFoundError:
        logger.error("YAML file not found at %s", config_path)
        sys.exit(1)
    except yaml.YAMLError as e:
        logger.error("Error parsing YAML file at %s: %s", config_path, e)
        sys.exit(1)
        
