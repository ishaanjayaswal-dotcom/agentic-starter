"""
Tiny HTTP API for the kernel.

Endpoints:
  GET  /health   -> {ok, skills}
  POST /dispatch -> body: {"goal": "..."}  -> job record
  GET  /jobs     -> list of job records
  GET  /jobs/N   -> one job record

Stdlib only. Run: python server.py
Default port 8765. No auth (local demo only).
"""

import json
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse

from orchestrator import dispatch, get_job, list_jobs
from skills import list_skills

HOST = "127.0.0.1"
PORT = 8765


class Handler(BaseHTTPRequestHandler):
    def log_message(self, fmt, *args):
        # Keep logs ASCII and short.
        print("[server] %s" % (fmt % args))

    def _send(self, code, payload):
        body = json.dumps(payload).encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        path = urlparse(self.path).path
        if path == "/health":
            self._send(200, {"ok": True, "skills": list_skills()})
            return
        if path == "/jobs":
            self._send(200, {"ok": True, "jobs": list_jobs()})
            return
        if path.startswith("/jobs/"):
            part = path[len("/jobs/") :].strip("/")
            try:
                job_id = int(part)
            except ValueError:
                self._send(400, {"ok": False, "error": "job id must be a number"})
                return
            job = get_job(job_id)
            if not job:
                self._send(404, {"ok": False, "error": "job not found"})
                return
            self._send(200, {"ok": True, "job": job})
            return
        self._send(404, {"ok": False, "error": "not found"})

    def do_POST(self):
        path = urlparse(self.path).path
        if path != "/dispatch":
            self._send(404, {"ok": False, "error": "not found"})
            return
        length = int(self.headers.get("Content-Length") or 0)
        raw = self.rfile.read(length) if length else b"{}"
        try:
            data = json.loads(raw.decode("utf-8") or "{}")
        except json.JSONDecodeError:
            self._send(400, {"ok": False, "error": "body must be JSON"})
            return
        goal = data.get("goal") or ""
        if not str(goal).strip():
            self._send(400, {"ok": False, "error": "goal is required"})
            return
        job = dispatch(str(goal))
        self._send(200, {"ok": True, "job": job})


def main():
    server = HTTPServer((HOST, PORT), Handler)
    print("[server] listening on http://%s:%s" % (HOST, PORT))
    print("[server] GET /health  POST /dispatch  GET /jobs")
    server.serve_forever()


if __name__ == "__main__":
    main()
