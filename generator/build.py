import json
import os
from jinja2 import Environment, FileSystemLoader

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

PROFILE = os.path.join(BASE_DIR, "profiles", "manuel-pulido.json")
TEMPLATE_DIR = os.path.join(BASE_DIR, "generator")
OUTPUT_DIR = os.path.join(BASE_DIR, "public")
OUTPUT_FILE = os.path.join(OUTPUT_DIR, "index.html")

# Crear entorno Jinja
env = Environment(loader=FileSystemLoader(TEMPLATE_DIR))
template = env.get_template("template.html")

# Leer perfil
with open(PROFILE, encoding="utf-8") as f:
    profile = json.load(f)

# Renderizar HTML
html = template.render(
    name=profile.get("name", ""),
    title=profile.get("subtitle", ""),
    description=profile.get("description", ""),
    links=profile.get("links", []),
    ga4=profile.get("ga_id", ""),
    meta_pixel=profile.get("meta_pixel", "")
)

# Asegurar carpeta public
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Guardar archivo
with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    f.write(html)

print("✅ Linktree generado correctamente")
print(f"📄 Archivo: {OUTPUT_FILE}")



