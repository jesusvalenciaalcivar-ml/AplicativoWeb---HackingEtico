# PROMPTS.md: registro de prompts

## A. Generación de la app (v0-ai-baseline)

La app «Mis tareas» la generó Claude Code (asistente de IA). El texto literal del prompt original no se conservó; en resumen, se pidió una aplicación web de una sola página en Flask para agregar y listar tareas, con las tareas guardadas en memoria, una plantilla Jinja2 y una prueba automática (`test_app.py`). *(Resumen reconstruido a partir del código entregado, no es el texto literal.)*

## B. Auditoría y remediación

**Prompt B1 (auditoría).** Se entregó a Claude el código de la app (`app.py`, `templates/index.html`, `requirements.txt`, `test_app.py`) junto con el enunciado del laboratorio y el reporte `REPORTE_VULNERABILIDADES.md`, con la orden de aplicar el ciclo descubrir, evaluar, priorizar, remediar y verificar.
Resultado: se ejecutaron pip-audit, Bandit, detect-secrets y cyclonedx-py sobre v0 y pruebas con curl sobre la app en marcha (`scans/before/`).

**Prompt B2 (remediación, resumen).** «Corrige los hallazgos con mejor relación riesgo/esfuerzo sin cambiar la funcionalidad: V-01 debug, V-02 límites y frecuencia, V-05 CSRF, V-04/V-06/V-07 cabeceras y los CVE de Werkzeug. V-03 (autenticación) queda como riesgo residual. Mantén las pruebas existentes y agrega pruebas para cada arreglo.»
Resultado de la IA: `werkzeug>=3.1.9`; `debug=False` con Waitress; `MAX_CONTENT_LENGTH`, `MAX_FORM_MEMORY_SIZE`, tope de 500 caracteres por nota y de 200 notas, Flask-Limiter (30 POST por minuto); Flask-WTF `CSRFProtect` con token en el formulario; cabeceras de seguridad en `after_request`.

**Verificación.** Se repitieron los mismos escaneos y pruebas sobre v1 (`scans/after/`) y `python test_app.py` imprime `OK`.
