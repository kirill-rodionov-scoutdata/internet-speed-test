import logging
from typing import Callable

import pytest

from speedtest import DEFAULT_URL, SpeedTest, main


def test_fetch_once_returns_elapsed_time_and_byte_count(
    speed_test: SpeedTest, mock_urlopen: Callable[[str], object], fake_response_bytes: bytes
) -> None:
    elapsed, size = speed_test.fetch_once()

    assert size == len(fake_response_bytes)
    assert elapsed >= 0


def test_process_collects_one_result_per_successful_request(
    speed_test: SpeedTest, mock_urlopen: Callable[[str], object], fake_response_bytes: bytes
) -> None:
    speed_test.process()

    assert len(speed_test.results) == speed_test.num_requests
    assert all(size == len(fake_response_bytes) for _, size in speed_test.results)


def test_process_exits_with_error_when_every_request_fails(
    speed_test: SpeedTest, mock_failing_urlopen: Callable[[str], None]
) -> None:
    with pytest.raises(SystemExit) as exit_info:
        speed_test.process()

    assert exit_info.value.code == 1
    assert speed_test.results == []


def test_report_exits_with_error_when_no_results(speed_test: SpeedTest) -> None:
    speed_test.results = []

    with pytest.raises(SystemExit) as exit_info:
        speed_test.report()

    assert exit_info.value.code == 1


def test_report_logs_average_speed_for_successful_requests(
    speed_test: SpeedTest, caplog: pytest.LogCaptureFixture
) -> None:
    speed_test.results = [(2.0, 4 * 1024 * 1024), (2.0, 4 * 1024 * 1024)]

    with caplog.at_level(logging.INFO):
        speed_test.report()

    assert "avg speed: 2.00 MB/s" in caplog.text


def test_main_uses_default_url_and_request_count_when_no_args_given(
    mock_speed_test_class: type, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setattr("sys.argv", ["speedtest.py"])

    main()

    instance = mock_speed_test_class.instances[0]
    assert instance["url"] == DEFAULT_URL
    assert instance["num_requests"] == 10
    assert instance["processed"] is True
