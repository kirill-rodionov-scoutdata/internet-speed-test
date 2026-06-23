import argparse
import logging
import sys
import time
import urllib.request

DEFAULT_URL = "https://raw.githubusercontent.com/kirill-rodionov-scoutdata/internet-speed-test/main/image.jpg"
CHUNK_SIZE = 64 * 1024

logger = logging.getLogger(__name__)


class SpeedTest:
    def __init__(self, url: str, num_requests: int) -> None:
        self.url = url
        self.num_requests = num_requests
        self.results: list[tuple[float, int]] = []

    def process(self) -> None:
        for attempt in range(1, self.num_requests + 1):
            try:
                elapsed, size = self.fetch_once()
            except OSError as exc:
                logger.warning("request %d/%d failed: %s", attempt, self.num_requests, exc)
                continue
            self.results.append((elapsed, size))
            logger.info(
                "request %d/%d: %.2fs, %.2f MB, %.2f MB/s",
                attempt, self.num_requests, elapsed, size / 1024**2, size / 1024**2 / elapsed,
            )
        self.report()

    def fetch_once(self) -> tuple[float, int]:
        start = time.monotonic()
        total_bytes = 0
        with urllib.request.urlopen(self.url) as response:
            while chunk := response.read(CHUNK_SIZE):
                total_bytes += len(chunk)
        return time.monotonic() - start, total_bytes

    def report(self) -> None:
        if not self.results:
            logger.error("all requests failed")
            sys.exit(1)
        durations = [elapsed for elapsed, _ in self.results]
        total_mb = sum(size for _, size in self.results) / 1024**2
        total_time = sum(durations)
        logger.info("summary: %d/%d succeeded", len(self.results), self.num_requests)
        logger.info("avg time: %.2fs", total_time / len(durations))
        logger.info("total downloaded: %.2f MB", total_mb)
        logger.info("avg speed: %.2f MB/s", total_mb / total_time)


def main() -> None:
    logging.basicConfig(level=logging.INFO, format="%(message)s")
    parser = argparse.ArgumentParser(description="Sequential HTTP download speed test.")
    parser.add_argument("url", nargs="?", default=DEFAULT_URL)
    parser.add_argument("-n", "--requests", type=int, default=10)
    args = parser.parse_args()
    SpeedTest(args.url, args.requests).process()


if __name__ == "__main__":
    main()
