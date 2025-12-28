import json
from pathlib import Path
from jinja2 import Environment, FileSystemLoader

BASE_DIR = Path(__file__).resolve().parent.parent
PROFILE_PATH = BASE_DIR / "profiles" / "manuel-pulido.json"
TEMPLATE_DIR = BASE_DIR / "generator"
PUBLIC_DIR = BASE_DIR / "public"

def build():
    if not PROFILE_PATH.exists():
        raise FileNotFoundError(f"No se encontró el perfil: {PROFILE_PATH}")

    with open(PROFILE_PATH, encoding="utf-8") as f:
        profile = json.load(f)

    env = Environment(
        loader=FileSystemLoader(TEMPLATE_DIR),
        autoescape=True
    )

    template = env.get_template("template.html")

    html = template.render(
        name=profile["name"],
        subtitle=profile["subtitle"],
        description=profile.get("description", ""),
        profile_image=profile["profile_image"],
        logo_image=profile["logo_image"],
        preload_image=profile["preload_image"],
        links=profile["links"],
        ga_id=profile.get("ga_id"),
        meta_pixel=profile.get("meta_pixel")
    )

    PUBLIC_DIR.mkdir(exist_ok=True)

    output = PUBLIC_DIR / "index.html"
    output.write_text(html, encoding="utf-8")

    print("✅ Linktree generado correctamente")
    print(f"📄 Archivo: {output}")

if __name__ == "__main__":
    build()


