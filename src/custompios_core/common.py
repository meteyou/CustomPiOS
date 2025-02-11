""" Common functions between CustomPiOS python scripts"""
from typing import Dict, Any, Optional, cast
import yaml
import os
from pathlib import Path

def get_custompios_folder():
    custompios_path = os.environ.get("CUSTOM_PI_OS_PATH", None)
    if custompios_path is not None:
        return Path(custompios_path)
    return Path(__file__).parent.parent


IMAGES_CONFIG = os.path.join(get_custompios_folder(), "images.yml")


def read_images() -> Dict[str, Dict[str,str]]:
    if not os.path.isfile(IMAGES_CONFIG):
        raise Exception(f"Error: Remotes config file not found: {IMAGES_CONFIG}")
    with open(IMAGES_CONFIG,'r') as f:
        output = yaml.safe_load(f)
        return output

def get_image_config() -> Optional[Dict["str", Any]]:
    images = read_images()

    print("get_image_config")

    base_board = os.environ.get("BASE_BOARD", None)
    base_image_path = os.environ.get("BASE_IMAGE_PATH", None)

    # remove any trailing spaces or line breaks
    if base_board is not None:
        base_board = base_board.strip()

    # Default to raspberrypiarmhf board in case of CustomPiOS v1
    if base_board is None:
        print("Warning: BASE_BOARD not set, defaulting to raspberrypiarmhf")
        base_board = "raspberrypiarmhf"

    if base_board in images["images"]:
        print(f"Using image config for board {base_board}")
        return images["images"][base_board]

    print("Error: Could not find image config for board '{}'\n".format(base_board))
    print(f"Available boards: {images['images'].keys()}")
    return None
