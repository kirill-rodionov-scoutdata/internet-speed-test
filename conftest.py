import io
from typing import Any, Callable

import pytest

from speedtest import SpeedTest


class FakeResponse:
    def __init__(self, data: bytes) -> None:
        self.stream = io.BytesIO(data)

    def read(self, size: int) -> bytes:
        return self.stream.read(size)

    def __enter__(self) -> "FakeResponse":
        return self

    def __exit__(self, *args: object) -> None:
        return None


class RecordingSpeedTest:
    instances: list[dict[str, Any]] = []

    def __init__(self, url: str, num_requests: int) -> None:
        self.url = url
        self.num_requests = num_requests
        self.processed = False
        RecordingSpeedTest.instances.append(vars(self))

    def process(self) -> None:
        self.processed = True


@pytest.fixture
def fake_response_bytes() -> bytes:
    return b"x" * (1024 * 1024)


@pytest.fixture
def mock_urlopen(monkeypatch: pytest.MonkeyPatch, fake_response_bytes: bytes) -> Callable[[str], FakeResponse]:
    def fake_urlopen(url: str) -> FakeResponse:
        return FakeResponse(fake_response_bytes)

    monkeypatch.setattr("speedtest.urllib.request.urlopen", fake_urlopen)
    return fake_urlopen


@pytest.fixture
def mock_failing_urlopen(monkeypatch: pytest.MonkeyPatch) -> Callable[[str], None]:
    def failing_urlopen(url: str) -> None:
        raise OSError("connection refused")

    monkeypatch.setattr("speedtest.urllib.request.urlopen", failing_urlopen)
    return failing_urlopen


@pytest.fixture
def speed_test() -> SpeedTest:
    return SpeedTest(url="https://example.com/image.jpg", num_requests=3)


@pytest.fixture
def mock_speed_test_class(monkeypatch: pytest.MonkeyPatch) -> type[RecordingSpeedTest]:
    RecordingSpeedTest.instances = []
    monkeypatch.setattr("speedtest.SpeedTest", RecordingSpeedTest)
    return RecordingSpeedTest
