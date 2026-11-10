from app import app, tareas

c = app.test_client()
assert b"No hay tareas" in c.get("/").data
c.post("/", data={"tarea": "  "})
assert tareas == [], "no debe guardar tareas vacías"
c.post("/", data={"tarea": "<b>comprar pan</b>"})
html = c.get("/").data
assert b"&lt;b&gt;comprar pan&lt;/b&gt;" in html, "el HTML debe escaparse"
print("OK")
