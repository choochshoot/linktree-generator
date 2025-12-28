from flask import Flask, render_template, request, redirect, url_for
import json
import subprocess
import os

# ===============================
# APP SETUP
# ===============================
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

app = Flask(
    __name__,
    static_folder=os.path.join(BASE_DIR, "public"),
    static_url_path="/static-preview"
)

PROFILE_PATH = os.path.join(BASE_DIR, "profiles", "manuel-pulido.json")
BUILD_SCRIPT = os.path.join(BASE_DIR, "generator", "build.py")

# Labels profesionales por posición
DEFAULT_LABELS = [
    "WhatsApp asesoría fiscal",
    "Nuestros servicios",
    "Agendar cita",
    "Leyes fiscales en México"
]

# ===============================
# ADMIN PANEL
# ===============================
@app.route("/", methods=["GET", "POST"])
def admin():
    # Leer perfil actual
    with open(PROFILE_PATH, encoding="utf-8") as f:
        profile = json.load(f)

    if request.method == "POST":
        # Datos básicos
        profile["name"] = request.form.get("name", "").strip()
        profile["subtitle"] = request.form.get("subtitle", "").strip()
        profile["description"] = request.form.get("description", "").strip()

        # Links (uno por línea)
        raw_links = request.form.get("links", "").split("\n")
        profile["links"] = [
            {
                "label": DEFAULT_LABELS[i] if i < len(DEFAULT_LABELS) else f"Link {i + 1}",
                "url": url.strip()
            }
            for i, url in enumerate(raw_links)
            if url.strip()
        ]

        # Tracking
        profile["ga_id"] = request.form.get("ga_id", "").strip()
        profile["meta_pixel"] = request.form.get("meta_pixel", "").strip()

        # Guardar JSON
        with open(PROFILE_PATH, "w", encoding="utf-8") as f:
            json.dump(profile, f, ensure_ascii=False, indent=2)

        # Regenerar Linktree
        subprocess.run(["python", BUILD_SCRIPT], check=True)

        return redirect(url_for("admin"))

    return render_template("admin.html", profile=profile)


# ===============================
# RUN
# ===============================
if __name__ == "__main__":
    app.run(debug=True)
