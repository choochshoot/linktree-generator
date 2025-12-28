import os

BASE_STRUCTURE = {
    "admin": {
        "templates": {
            "admin.html": ""
        },
        "static": {
            "admin.css": ""
        },
        "app.py": ""
    },
    "generator": {
        "template.html": "",
        "build.py": ""
    },
    "profiles": {
        "manuel-pulido.json": """{
  "slug": "manuel-pulido",
  "name": "Manuel Pulido",
  "title": "Abogado Fiscal",
  "whatsapp": {
    "number": "5215618371510",
    "cta_main": "Hola Lic. Manuel, me interesan sus servicios de asesoría fiscal.",
    "cta_appointment": "Deseo hacer una cita."
  },
  "services": [
    "Asesoría fiscal integral",
    "Defensa ante el SAT",
    "Planeación fiscal",
    "Cumplimiento fiscal"
  ],
  "laws_url": "https://www.gob.mx/sat/documentos/leyes-fiscales",
  "tracking": {
    "ga4": "",
    "meta_pixel": ""
  }
}"""
    },
    "public": {
        "index.html": "",
        "assets": {
            "css": {
                "style.css": ""
            },
            "images": {
                "profile.jpg": "",
                "logo.jpg": "",
                "preload.jpg": ""
            }
        }
    },
    "README.md": "# Linktree Generator\n\nProyecto base para generar linktrees profesionales.",
    "requirements.txt": "flask\n",
    ".gitignore": "__pycache__/\n.env\n"
}


def create_structure(base_path, structure):
    for name, content in structure.items():
        path = os.path.join(base_path, name)

        if isinstance(content, dict):
            os.makedirs(path, exist_ok=True)
            create_structure(path, content)
        else:
            if not os.path.exists(path):
                with open(path, "w", encoding="utf-8") as f:
                    f.write(content)


if __name__ == "__main__":
    print("🚀 Inicializando estructura del proyecto...\n")
    create_structure(".", BASE_STRUCTURE)
    print("✅ Estructura creada correctamente")
