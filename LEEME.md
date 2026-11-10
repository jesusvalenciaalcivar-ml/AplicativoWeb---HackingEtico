# Cómo usar esta carpeta en tu repo

1. En tu repo (código original, sin tocar): `git tag v0-ai-baseline`
2. Copia a tu repo estos archivos: `app.py`, `templates/index.html`, `requirements.txt`, `test_app.py`, la carpeta `scans/`, `findings.csv` y `PROMPTS.md`.
3. `pip install -r requirements.txt` y `python test_app.py` (debe imprimir OK).
4. `git add -A && git commit -m "Remediacion v1" && git tag v1-remediated`
5. `git push && git push --tags`
6. Exporta el informe a PDF como `Week8_AIAppAudit_Alcivar.pdf` y entrégalo con el link del repo.
