"""Utility functions like saving and loading YAML files."""
from pathlib import Path

import yaml

from . import StreamInfo


def load(filename: Path | str) -> None:
    """Load the yaml file and return it as StreamInfo."""
    with open(filename, 'r') as data:
        yaml_data = yaml.safe_load(data)
        return [StreamInfo(**stream) for stream in yaml_data]
    return None
