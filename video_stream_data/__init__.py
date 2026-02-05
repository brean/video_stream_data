"""Provide unified meta data definition for video streaming."""
from dataclasses import asdict, dataclass, field
from enum import Enum


class StreamControlType(str, Enum):
    """Different configuration types for the stream.

    Taken from opencv2 device controls.
    """

    INT = 'int'
    BOOL = 'bool'
    MENU = 'menu'


class Encoding(str, Enum):
    """Defines how the video stream gets encodied.

    Should default to 'passthrough'.
    Normally BGR in ROS, RGB in h264.
    """

    PASSTHROUGH = 'passthrough'
    BGR = 'bgr'
    GREY = 'grey'
    GREY16 = 'grey16'
    RGB = 'rgb'
    BGRA = 'bgra'
    RGBA = 'rgba'

    def to_ros_bridge(self) -> str:
        """Create string to use with the ROS2 CvBridge."""
        if self.value == Encoding.BGR:
            return 'bgr8'
        elif self.value == Encoding.RGB:
            return 'rgb8'
        elif self.value == Encoding.BGR:
            return 'bgra8'
        elif self.value == Encoding.RGB:
            return 'rgba8'
        elif self.value == Encoding.GREY:
            return 'mono8'
        elif self.value == Encoding.GREY16:
            return 'mono16'
        else:
            return str(self.value)


class Codec(str, Enum):
    """Codec type/Pixel format as fourcc."""

    # see linuxpy/video/raw.py

    MJPEG = 'MJPEG'  # Motion-JPEG
    YUYV = 'YUYV'
    XVID = 'XVID'  # MP4 files
    UNKNOWN = 'unknown'

    def to_text(self) -> str:
        """Create human readable text."""
        if self.value == Encoding.MJPEG:
            return 'Motion-JPEG'
        elif self.value == Encoding.YUYV:
            return 'YUYV'
        elif self.value == Encoding.XVID:
            return 'XVID/MP4'

    def to_fourcc(self) -> str:
        """Create FourCC-Text for configuration of OpenCV2 VideoWriter."""
        if self.value == Encoding.MJPEG:
            return 'MJPG'
        return str(self)


@dataclass
class StreamControl:
    """Provide a value the user can configure."""

    type: StreamControlType  # noqa: A003
    name: str
    writable: bool = False
    min: float = 0  # noqa: A003
    max: float = 0  # noqa: A003
    step: int = 1
    value: int | float | bool | None = None
    options: list[(str, str)] = field(default_factory=list)

    def __post_init__(self):
        if self.type:
            self.type = StreamControlType(self.type)

@dataclass
class StreamValue:
    """Values requested by the user."""

    # selected resolution
    resolution: list[int]
    # current fps
    fps: float
    # selected control configurations
    controls: dict[str, int | float | bool | None]
    # selected encoding, e.g. bgr
    encoding: Encoding = Encoding.PASSTHROUGH
    # selected codec e.g. MJPEG for "Motion-JPEG" or YUYV for "YUYV 4:2:2"
    codec: Codec = Codec.UNKNOWN

    def __post_init__(self):
        if self.encoding:
            self.encoding = Encoding(self.encoding)


@dataclass
class StreamInfo:
    """Stream information provided by the device/host."""

    name: str
    # unique stream path
    stream_path: str
    # driver for example "uvcvideo" for a local OpenCV webcam or
    # "webrtc" for a WebRTC Video Stream
    driver: str
    # available codec
    codec: list[Codec]
    # all available controls from linuxpy
    controls: list[StreamControl]
    # all available resolutions, starting with the default resolution
    resolutions: list[int, int]
    # max. possible fps (at default resolution)
    max_fps: float
    # current configuration as own data structure so it can easily be handed
    # over as dict from any service
    values: StreamValue
    backend: str = 'v4l2'  # (optional) OpenCV2 Backend (only if cv2 is used)

    def __post_init__(self):
        if self.codec:
            self.codec = [Codec(c) for c in self.codec]
        if self.values and isinstance(self.values, dict):
            self.values = StreamValue(**self.values)
        if self.controls:
            self.controls = [
                StreamControl(**c) if isinstance(c, dict) else c
                for c in self.controls
            ]


def _dict_factory(data):
    def convert_value(obj):
        if isinstance(obj, Enum):
            return obj.value
        elif isinstance(obj, list):
            return [convert_value(x) for x in obj]
        elif isinstance(obj, set):
            return {convert_value(x) for x in obj}
        elif isinstance(obj, tuple):
            return tuple(convert_value(x) for x in obj)
        return obj
    return {k: convert_value(v) for k, v in data}


def stream_as_dict(stream_obj):
    """Serialize stream information as dict."""
    return asdict(
        stream_obj,
        dict_factory=_dict_factory)
