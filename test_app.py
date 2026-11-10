from app import app, tareas, MAX_LARGO_TAREA

# --- pruebas originales (sin CSRF, para probar solo la lógica) ---
app.config["WTF_CSRF_ENABLED"] = False
c = app.test_client()
assert b"No hay tareas" in c.get("/").data
c.post("/", data={"tarea": "  "})
assert tareas == [], "no debe guardar tareas vacías"
c.post("/", data={"tarea": "<b>comprar pan</b>"})
html = c.get("/").data
assert b"&lt;b&gt;comprar pan&lt;/b&gt;" in html, "el HTML debe escaparse"

# --- V-02: tarea demasiado larga se rechaza ---
assert c.post("/", data={"tarea": "A" * (MAX_LARGO_TAREA + 1)}).status_code == 400
assert c.post("/", data={"tarea": "A" * 400000}).status_code == 413

# --- V-06 / V-07 / V-04: cabeceras de seguridad ---
r = c.get("/")
assert r.headers["X-Frame-Options"] == "DENY"
assert r.headers["X-Content-Type-Options"] == "nosniff"
assert "frame-ancestors" in r.headers["Content-Security-Policy"]
assert "Werkzeug" not in r.headers["Server"]

# --- V-05: con CSRF activo, un POST sin token se rechaza ---
app.config["WTF_CSRF_ENABLED"] = True
c2 = app.test_client()
assert c2.post("/", data={"tarea": "csrf"}).status_code == 400
print("OK")
