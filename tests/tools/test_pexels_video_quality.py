from unittest.mock import Mock, patch

from tools.video.pexels_video import PexelsVideo


def test_quality_missing_selects_hd_mp4_not_first_preview(tmp_path, monkeypatch):
    monkeypatch.setenv('PEXELS_API_KEY', 'test-only')
    search = Mock()
    search.json.return_value = {'videos': [{'id': 123, 'duration': 20, 'video_files': [
        {'width': 640, 'height': 360, 'link': 'preview', 'file_type': 'video/mp4'},
        {'width': 3840, 'height': 2160, 'link': '4k', 'file_type': 'video/mp4'},
        {'width': 1920, 'height': 1080, 'link': 'hd', 'file_type': 'video/mp4'},
    ]}]}
    download = Mock(content=b'test-video')
    with patch('requests.get', side_effect=[search, download]) as get:
        result = PexelsVideo().execute({'query': 'road', 'output_path': str(tmp_path / 'road.mp4')})
    assert result.success
    assert result.data['width'] == 1920
    assert get.call_args_list[1].args[0] == 'hd'


def test_explicit_quality_still_has_priority(tmp_path, monkeypatch):
    monkeypatch.setenv('PEXELS_API_KEY', 'test-only')
    search = Mock()
    search.json.return_value = {'videos': [{'id': 123, 'duration': 20, 'video_files': [
        {'width': 1920, 'height': 1080, 'link': 'unclassified'},
        {'width': 1280, 'height': 720, 'link': 'classified-hd', 'quality': 'hd'},
    ]}]}
    with patch('requests.get', side_effect=[search, Mock(content=b'test-video')]) as get:
        result = PexelsVideo().execute({'query': 'metro', 'output_path': str(tmp_path / 'metro.mp4')})
    assert result.success
    assert get.call_args_list[1].args[0] == 'classified-hd'
