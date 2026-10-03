"""Static file server with HTTP Range support, so a browser (e.g. Playwright, which
blocks file://) can seek in a big WAV. Python's http.server ignores Range headers.

  python scripts/non_essential/range_server.py output/<dir> 8766
  -> http://127.0.0.1:8766/edit_review/studio.html

Runs until stopped; runtime is whatever you leave it for. Logs nothing.
"""
import os
import sys
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer

ROOT, PORT = sys.argv[1], int(sys.argv[2])


class RangeHandler(SimpleHTTPRequestHandler):
    def __init__(self, *a, **k):
        super().__init__(*a, directory=ROOT, **k)

    def send_head(self):
        rng = self.headers.get("Range")
        path = self.translate_path(self.path)
        if not rng or not os.path.isfile(path):
            return super().send_head()
        size = os.path.getsize(path)
        start, _, end = rng.replace("bytes=", "").partition("-")
        start = int(start or 0)
        end = min(int(end) if end else size - 1, size - 1)
        f = open(path, "rb")
        f.seek(start)
        self.send_response(206)
        self.send_header("Content-Type", self.guess_type(path))
        self.send_header("Accept-Ranges", "bytes")
        self.send_header("Content-Range", f"bytes {start}-{end}/{size}")
        self.send_header("Content-Length", str(end - start + 1))
        self.end_headers()
        self._remaining = end - start + 1
        return f

    def copyfile(self, src, dst):
        left = getattr(self, "_remaining", None)
        if left is None:
            return super().copyfile(src, dst)
        while left > 0:
            chunk = src.read(min(65536, left))
            if not chunk:
                break
            try:
                dst.write(chunk)
            except (BrokenPipeError, ConnectionResetError):
                break
            left -= len(chunk)

    def log_message(self, *a):
        pass


ThreadingHTTPServer(("127.0.0.1", PORT), RangeHandler).serve_forever()
