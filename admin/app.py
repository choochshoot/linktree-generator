from flask import Flask, render_template, request, redirect, url_for
import json
import os
import subprocess

# ===============================
# CONFIGURACIÓN
# ===============================
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

PROFILE_PATH = os.path.join(BASE_DIR, "..", "profiles", "manuel-pulido.json")
GENERATOR_SCRIPT = os.path.join(BASE_DIR, "..", "generator", "build.py")
IMAGES_PATH = os.path.join(BASE_DIR, "..", "public", "assets", "images")

ALLOWED_IMAGES = {
    "profile": "profile.jpg",
    "logo": "logo.jpg",
    "preload": "preload.jpg"
}

app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = 5 * 1024 * 1024  # 5MB


# ===============================
# HELPERS
# ===============================
def load_profile():
    with open(PROFILE_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def save_profile(profile):
    with open(PROFILE_PATH, "w", encoding="utf-8") as f:
        json.dump(profile, f, indent=2, ensure_ascii=False)


def generate_linktree():
    subprocess.run(
        ["python", GENERATOR_SCRIPT],
        cwd=os.path.dirname(GENERATOR_SCRIPT),
        check=True
    )


# ===============================
# ROUTES
# ===============================
@app.route("/", methods=["GET", "POST"])
def admin_panel():
    profile = load_profile()

    if request.method == "POST":
        # ---- Datos básicos ----
        profile["name"] = request.form.get("name", "").strip()
        profile["title"] = request.form.get("title", "").strip()

        # ---- WhatsApp ----
        profile["whatsapp"]["number"] = request.form.get("whatsapp", "").strip()
        profile["whatsapp"]["cta_main"] = request.form.get("cta_main", "").strip()
        profile["whatsapp"]["cta_appointment"] = request.form.get("cta_appointment", "").strip()

        # ---- Servicios ----
        services_raw = request.form.get("services", "")
        profile["services"] = [s.strip() for s in services_raw.split(",") if s.strip()]

        # ---- Links ----
        profile["laws_url"] = request.form.get("laws_url", "").strip()

        # ---- Tracking ----
        profile["tracking"]["ga4"] = request.form.get("ga4", "").strip()
        profile["tracking"]["meta_pixel"] = request.form.get("meta_pixel", "").strip()

        # ---- Imágenes ----
        os.makedirs(IMAGES_PATH, exist_ok=True)

        for field, filename in ALLOWED_IMAGES.items():
            file = request.files.get(field)
            if file and file.filename:
                file.save(os.path.join(IMAGES_PATH, filename))

        # ---- Guardar y generar ----
        save_profile(profile)
        generate_linktree()

        return redirect(url_for("admin_panel"))

    return render_template("admin.html", profile=profile)


# ===============================
# MAIN
# ===============================
if __name__ == "__main__":
    print("🟢 Panel Admin iniciado")
    print("👉 http://127.0.0.1:5000")
    app.run(debug=True)
