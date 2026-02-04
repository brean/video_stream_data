"""Test loading/saving data."""
from pathlib import Path
import tempfile

from video_stream_data import Codec, Encoding, StreamInfo, StreamValue
from video_stream_data.utils import load, save

BASE_PATH = Path(__file__).absolute().parent
LOCAL_VIDEO_DEVICE = BASE_PATH / 'data' / 'local_video_device.yml'


def test_load_stream_info():
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


def test_save_stream_info():
    """Test saving data to temp file."""
    stream_info = load(LOCAL_VIDEO_DEVICE)
    tmp = tempfile.NamedTemporaryFile()
    save(stream_info, tmp.name)

    # check file by string compare
    saved_data = ''
    with open(tmp.name, 'r') as data:
        saved_data = data.read()
    assert 'Dummy Camera' in saved_data

    # check full structure by reloading
    reloaded_stream_info = load(tmp.name)
    assert reloaded_stream_info == stream_info
