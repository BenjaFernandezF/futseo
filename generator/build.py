import json
import os
import re
from pathlib import Path
from datetime import datetime
ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "matches.json"
DOCS = ROOT / "docs"
OUT_MATCH = DOCS / "partido"

def slugify(text: str) -> str:
    text = text.lower().strip()
    text = re.sub(r"[^\w\s-]", "", text, flags=re.UNICODE)
    text = re.sub(r"[\s_-]+", "-", text)
    return text.strip("-")
def match_filename(m: dict) -> str:
    base = f"{m['home']} vs {m['away']} {m['date']} {m['league_slug']}"
    return slugify(base) + ".html"
def render_match(m: dict) -> str:
    s = m["stats"]
    title = f"{m['home']} vs {m['away']} – Estadísticas y análisis"
    desc = f"{m['home']} vs {m['away']}: estadísticas, xG, remates, posesión y resumen del partido."
    return f"""<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8" />
  <title>{title}</title>
  <meta name="description" content="{desc}">
  <meta name="viewport" content="width=device-width, initial-scale=1">
</head>
<body>
  <a href="../index.html">← Volver al inicio</a>
<h1>{m['home']} vs {m['away']}</h1>
  <p><b>Liga:</b> {m['league']}</p>
  <p><b>Fecha:</b> {m['date']}</p>
  <p><b>Marcador:</b> {m['score']}</p>

  <h2>Resumen</h2>
  <p>Resumen automático (por ahora básico). Luego lo haremos con plantillas y reglas.</p>

  <h2>Estadísticas</h2>
  <table border="1" cellpadding="6">
    <tr><th>Métrica</th><th>Local</th><th>Visita</th></tr>
    <tr><td>xG</td><td>{s['xg_home']}</td><td>{s['xg_away']}</td></tr>
    <tr><td>Remates</td><td>{s['shots_home']}</td><td>{s['shots_away']}</td></tr>
    <tr><td>Posesión</td><td>{s['pos_home']}%</td><td>{s['pos_away']}%</td></tr>
  </table>
</body>
</html>
"""
def render_home(items: list[tuple[str, dict]]) -> str:
    links = "\n".join([f'<li><a href="partido/{fn}">{m["home"]} vs {m["away"]} ({m["league"]}, {m["date"]})</a></li>' for fn, m in items])
    return f"""<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8">
  <title>FutData – Estadísticas de fútbol</title>
  <meta name="description" content="Estadísticas y análisis de partidos de fútbol. Premier League, Serie A y Liga MX.">
  <meta name="viewport" content="width=device-width, initial-scale=1">
</head>
<body>
  <h1>FutData</h1>
  <p>SEO puro. Páginas automáticas por partido.</p>

  <h2>Últimos partidos (auto)</h2>
  <ul>
    {links}
  </ul>
<p><i>Próximo paso: reemplazar estos datos mock por 365Scores.</i></p>
</body>
</html>
"""

def main():
    DOCS.mkdir(exist_ok=True)
    OUT_MATCH.mkdir(parents=True, exist_ok=True)

    matches = json.loads(DATA.read_text(encoding="utf-8"))
    generated = []

    for m in matches:
        fn = match_filename(m)
        (OUT_MATCH / fn).write_text(render_match(m), encoding="utf-8")
        generated.append((fn, m))

    (DOCS / "index.html").write_text(render_home(generated), encoding="utf-8")
    print(f"Generadas {len(generated)} paginas de partido + index.html")

if __name__ == "__main__":
    main()
