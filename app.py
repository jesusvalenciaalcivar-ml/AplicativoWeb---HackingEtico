import os
import secrets

from flask import Flask, abort, redirect, render_template, request, url_for
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_wtf.csrf import CSRFProtect

MAX_LARGO_TAREA = 500   # caracteres por tarea
MAX_TAREAS = 200        # tareas guardadas en memoria

app = Flask(__name__)
# Clave para firmar el token CSRF: se toma del entorno; si no existe, se genera una al arrancar
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY") or secrets.token_hex(32)
app.config["SESSION_COOKIE_SAMESITE"] = "Lax"
# V-02: límites de tamaño de la petición (20 KB en total, 10 KB por formulario)
app.config["MAX_CONTENT_LENGTH"] = 20_000
app.config["MAX_FORM_MEMORY_SIZE"] = 10_000

# V-05: protección CSRF para todos los formularios
csrf = CSRFProtect(app)
# V-02: limitar la frecuencia de peticiones por dirección IP
limiter = Limiter(get_remote_address, app=app, storage_uri="memory://")

# shortcut: tareas en memoria, se pierden al reiniciar; usar SQLite si hay que guardarlas
tareas = []


@app.after_request
def cabeceras_de_seguridad(resp):
    # V-06 y V-07: cabeceras que faltaban; V-04: ocultar la versión del servidor
    resp.headers["X-Frame-Options"] = "DENY"
    resp.headers["X-Content-Type-Options"] = "nosniff"
    resp.headers["Referrer-Policy"] = "no-referrer"
    resp.headers["Content-Security-Policy"] = (
        "default-src 'self'; style-src 'self' 'unsafe-inline'; frame-ancestors 'none'"
    )
    resp.headers["Server"] = "app"
    return resp


@app.route("/", methods=["GET", "POST"])
@limiter.limit("30 per minute", methods=["POST"])
def index():
    if request.method == "POST":
        texto = request.form.get("tarea", "").strip()
        if len(texto) > MAX_LARGO_TAREA or len(tareas) >= MAX_TAREAS:
            abort(400)
        if texto:
            tareas.append(texto)
        return redirect(url_for("index"))
    return render_template("index.html", tareas=tareas)


if __name__ == "__main__":
    # V-01: sin modo debug y con un servidor de producción (Waitress)
    from waitress import serve
    serve(app, host="127.0.0.1", port=5000)
