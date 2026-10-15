# ------------------------------------------------
# Author: Marcos Tello
# Date: October 2026
# ------------------------------------------------

"""Proxy local para Rubin Crossmatch Lab (solo biblioteca estándar).
"""
import http.server, os, ssl, sys, urllib.error, urllib.parse, urllib.request, webbrowser

PORT = int(sys.argv[1]) if len(sys.argv) > 1 else 8765
HERE = os.path.dirname(os.path.abspath(__file__))
PAGE = os.path.join(HERE, "rubin_crossmatch_lab_local.html")
HOSTS = {
    "tap.alerce.online",            # ALeRCE TAP (Rubin)
    "cdsxmatch.u-strasbg.fr",       # CDS xmatch (Gaia DR3, AllWISE, ...)
    "cdsxmatch.cds.unistra.fr",
    "gea.esac.esa.int",             # Gaia Archive TAP
    "tapvizier.cds.unistra.fr",     # VizieR TAP
    "www.wis-tns.org",              # TNS API
    "sandbox.wis-tns.org",
}

# Hosts con credenciales: nunca se acepta un certificado sin verificar.
NO_INSECURE = {"www.wis-tns.org", "sandbox.wis-tns.org"}
STRICT = os.environ.get("RUBIN_PROXY_STRICT") == "1"   # =1 desactiva el modo sin verificar


def _contexts(host):
    """Contextos TLS a probar en orden: sistema -> certifi -> (solo datos publicos) sin verificar.
    Python en Windows suele no traer los certificados intermedios que el navegador si usa."""
    ctxs = [ssl.create_default_context()]
    try:
        import certifi
        ctxs.append(ssl.create_default_context(cafile=certifi.where()))
    except ImportError:
        pass
    if host not in NO_INSECURE and not STRICT:
        u = ssl.create_default_context()
        u.check_hostname, u.verify_mode = False, ssl.CERT_NONE
        ctxs.append(u)
    return ctxs


class Handler(http.server.BaseHTTPRequestHandler):
    def _send(self, code, body, ctype="text/plain; charset=utf-8"):
        if isinstance(body, str):
            body = body.encode()
        self.send_response(code)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _relay(self, method):
        q = urllib.parse.parse_qs(urllib.parse.urlparse(self.path).query)
        url = q.get("url", [""])[0]
        p = urllib.parse.urlparse(url)
        if p.scheme not in ("http", "https") or p.hostname not in HOSTS:
            return self._send(403, f"Host no permitido: {p.hostname}")
        n = int(self.headers.get("Content-Length") or 0)
        data = self.rfile.read(n) if n else None
        hdr = {"User-Agent": self.headers.get("X-Upstream-UA") or "rubin-crossmatch-lab/1.0"}
        if self.headers.get("Content-Type"):
            hdr["Content-Type"] = self.headers["Content-Type"]
        ctxs = _contexts(p.hostname) if p.scheme == "https" else [None]
        err = None
        for i, ctx in enumerate(ctxs):
            req = urllib.request.Request(url, data=data, headers=hdr, method=method)
            try:
                with urllib.request.urlopen(req, timeout=900, context=ctx) as r:
                    if ctx is not None and ctx.verify_mode == ssl.CERT_NONE:
                        sys.stderr.write(f"[proxy] aviso: {p.hostname} sin verificar certificado (datos publicos)\n")
                    return self._send(r.status, r.read(), r.headers.get("Content-Type", "text/plain"))
            except urllib.error.HTTPError as e:
                return self._send(e.code, e.read())
            except urllib.error.URLError as e:
                err = e
                if isinstance(e.reason, ssl.SSLError) and i + 1 < len(ctxs):
                    continue
                break
            except Exception as e:  # DNS, timeout, reset...
                err = e
                break
        hint = " (TNS exige certificado valido: ejecuta 'pip install certifi')" if (
            p.hostname in NO_INSECURE and "CERTIFICATE" in str(err)) else ""
        self._send(502, f"{type(err).__name__}: {err}{hint}")

    def do_GET(self):
        path = urllib.parse.urlparse(self.path).path
        if path == "/api/ping":
            return self._send(200, "rubin-proxy")
        if path == "/api/proxy":
            return self._relay("GET")
        if path in ("/", "/index.html"):
            if not os.path.exists(PAGE):
                return self._send(404, "Falta rubin_crossmatch_lab_local.html junto a este script.")
            return self._send(200, open(PAGE, "rb").read(), "text/html; charset=utf-8")
        self._send(404, "No encontrado")

    def do_POST(self):
        if urllib.parse.urlparse(self.path).path == "/api/proxy":
            return self._relay("POST")
        self._send(404, "No encontrado")

    def log_message(self, fmt, *a):
        sys.stderr.write("[proxy] " + fmt % a + "\n")


if __name__ == "__main__":
    srv = http.server.ThreadingHTTPServer(("127.0.0.1", PORT), Handler)
    print(f"Rubin Crossmatch Lab -> http://localhost:{PORT}  (Ctrl+C para salir)")
    try:
        webbrowser.open(f"http://localhost:{PORT}")   # abre la direccion correcta
    except Exception:
        pass
    try:
        srv.serve_forever()
    except KeyboardInterrupt:
        pass
