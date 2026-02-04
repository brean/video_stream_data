"""Test loading/saving data."""
from pathlib import Path

from video_stream_data import Codec, Encoding, StreamInfo, StreamValue
from video_stream_data.utils import load

BASE_PATH = Path(__file__).absolute().parent
LOCAL_VIDEO_DEVICE = BASE_PATH / 'data' / 'local_video_device.yml'


def test_stream_info():
    """Test loading data from yaml."""
    stream_info = load(LOCAL_VIDEO_DEVICE)
    assert len(stream_info) == 1
    stream = stream_info[0]
    assert isinstance(stream, StreamInfo)
    assert stream.name == 'Dummy Camera'
    assert isinstance(stream.values, StreamValue)
    assert stream.values.codec == Codec.MJPEG
    assert stream.values.encoding == Encoding.PASSTHROUGH
    assert stream.values.controls['Power Line Frequency'] == 2
    assert stream.controls
    power_line_freq = False
    for ctrl in stream.controls:
        if ctrl.name == 'Power Line Frequency':
            power_line_freq = True
            break
    assert power_line_freq
