"""Utility functions like saving and loading YAML files."""
from pathlib import Path

import yaml

from . import stream_as_dict, StreamInfo


def load(filename: Path | str) -> None | list[StreamInfo]:
    """Load the yaml file and return it as list of StreamInfo."""
    with open(filename, 'r') as data:
        yaml_data = yaml.safe_load(data)
        return [StreamInfo(**stream) for stream in yaml_data]
    return None


def save(data: list[StreamInfo], filename: Path | str) -> None:
    """Save list of StreamInfo to yaml file."""
    yaml_data = [stream_as_dict(s) for s in data]
    with open(filename, 'w') as data:
        data.write(yaml.safe_dump(yaml_data))
