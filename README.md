# Video Stream Data
Dependency-free data structures for video streaming.

## Installation
Use **pip** to install. Its recommended to install in a virtual environment

```bash
python3 -m venv video-streaming-pipeline
# install using system-site-packages (like opencv and pyudev)
source video-streaming-pipeline/bin/activate --system-site-packages
pip3 install video_stream_data
```

Although not recommended a user installation with `--break-system-packages` would also be okay as it does not have any dependencies.

## Usage
Simply import the data classes you want to have, you can use the parser to load the video stream settings from a file (see `test/`-folder).

You can use the data structure to manually create any kind of video stream.


```mermaid
classDiagram
    direction LR

    class StreamControlType {
        <<enumeration>>
        +INT: str = 'int'
        +BOOL: str = 'bool'
        +MENU: str = 'menu'
    }

    class Encoding {
        <<enumeration>>
        +BGR: str = 'bgr'
        +GREY: str = 'grey'
        +GREY16: str = 'grey16'
        +GRB: str = 'rbg'
        +BGRA: str = 'bgra'
        +RGBA: str = 'rgba'

    }

    class Codec {
        <<enumeration>>
        +MJPG: str = 'MJPG'  # Motion-JPEG
        +YUYV: str = 'YUYV'  # 'YUYV 4:2:2'
        +XVID: str = 'XVID'
    }

    class StreamControl {
        +type: StreamControlType
        +name: str
        +writable: bool
        +min: float
        +max: float
        +step: int
        +value: float | bool | None
        +options: list
    }

    class StreamValue {
        +resolution: list
        +fps: float
        +controls: list[StreamControl]
        +encoding: Encoding
        +codec: Codec
    }

    class StreamInfo {
        +name: str
        +stream_path: str
        +driver: str
        +codec: list[str]
        +controls: list[StreamControl]
        +resolutions: list[int, int]
        +max_fps: float
        +values: StreamValue
        +backend: str = 'v4l2'
    }

    StreamControlType <|-- StreamControl
    Encoding <|-- StreamValue
    Codec <|-- StreamValue
    StreamControl --> StreamInfo : controls
    StreamValue --> StreamInfo : values

```
*Fig. 1: Data Model for the StreamInfo generated from any device*
