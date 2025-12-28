import json
import os

# ===============================
# RUTAS ABSOLUTAS SEGURAS
# ===============================
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

PROFILE_PATH = os.path.join(BASE_DIR, "profiles", "manuel-pulido.json")
TEMPLATE_PATH = os.path.join(BASE_DIR, "generator", "template.html")
OUTPUT_PATH = os.path.join(BASE_DIR, "public", "index.html")

# ===============================
# CARGA DE ARCHIVOS
# ===============================
with open(PROFILE_PATH, encoding="utf-8") as f:
    data = json.load(f)

with open(TEMPLATE_PATH, encoding="utf-8") as f:
    html = f.read()

# ===============================
# GENERACIÓN DE CONTENIDO
# ===============================
services_html = "".join(f"<li>{s}</li>" for s in data["services"])

wa_main = (
    f"https://wa.me/{data['whatsapp']['number']}?"
    f"text={data['whatsapp']['cta_main']}"
)

wa_appointment = (
    f"https://wa.me/{data['whatsapp']['number']}?"
    f"text={data['whatsapp']['cta_appointment']}"
)

# ===============================
# TRACKING (OPCIONAL)
# ===============================
ga_id = data.get("tracking", {}).get("ga4")
meta_id = data.get("tracking", {}).get("meta_pixel")

ga_script = ""
if ga_id:
    ga_script = f"""
<script async src="https://www.googletagmanager.com/gtag/js?id={ga_id}"></script>
<script>
window.dataLayer = window.dataLayer || [];
function gtag(){{dataLayer.push(arguments);}}
gtag('js', new Date());
gtag('config', '{ga_id}');
</script>
"""

meta_script = ""
if meta_id:
    meta_script = f"""
<script>
!function(f,b,e,v,n,t,s){{
if(f.fbq)return;n=f.fbq=function(){{
n.callMethod?n.callMethod.apply(n,arguments):n.queue.push(arguments)}};
if(!f._fbq)f._fbq=n;n.push=n;n.loaded=!0;n.version='2.0';
n.queue=[];t=b.createElement(e);t.async=!0;
t.src=v;s=b.getElementsByTagName(e)[0];
s.parentNode.insertBefore(t,s)
}}(window,document,'script','https://connect.facebook.net/en_US/fbevents.js');
fbq('init','{meta_id}');
fbq('track','PageView');
</script>
"""

# ===============================
# REEMPLAZOS
# ===============================
html = html.replace("{{NAME}}", data["name"])
html = html.replace("{{TITLE}}", data["title"])
html = html.replace("{{SERVICES}}", services_html)
html = html.replace("{{WHATSAPP_MAIN}}", wa_main)
html = html.replace("{{WHATSAPP_APPOINTMENT}}", wa_appointment)
html = html.replace("{{LAWS_URL}}", data["laws_url"])
html = html.replace("{{GA_SCRIPT}}", ga_script)
html = html.replace("{{META_SCRIPT}}", meta_script)

# ===============================
# OUTPUT
# ===============================
with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
    f.write(html)

print("✅ Linktree generado correctamente")
print(f"📄 Archivo generado: {OUTPUT_PATH}")
