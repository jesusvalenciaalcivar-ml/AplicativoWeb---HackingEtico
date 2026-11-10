from flask import Flask, redirect, render_template, request, url_for

app = Flask(__name__)
# shortcut: tareas en memoria, se pierden al reiniciar; usar SQLite si hay que guardarlas
tareas = []


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        texto = request.form.get("tarea", "").strip()
        if texto:
            tareas.append(texto)
        return redirect(url_for("index"))
    return render_template("index.html", tareas=tareas)


if __name__ == "__main__":
    app.run(debug=True)
