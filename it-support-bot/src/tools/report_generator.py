"""Tool: generate professional IT support reports."""

import os
import re
from datetime import datetime
from pathlib import Path
from crewai.tools import tool

# Output directory for reports — sandboxed
REPORTS_DIR = Path(os.getenv("IT_SUPPORT_OUTPUT", "./reports")).resolve()


@tool("GenerateSupportReport")
def generate_support_report(
    client_name: str,
    issue_description: str,
    diagnosis: str,
    solution: str,
    steps_performed: str,
    recommendations: str = "",
) -> str:
    """
    Genera un reporte profesional de soporte IT.
    Recibe: nombre del cliente, descripción del problema, diagnóstico,
    solución aplicada, pasos realizados y recomendaciones adicionales.
    Devuelve la ruta del archivo generado.
    """
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
    report_id = datetime.now().strftime("%Y%m%d_%H%M%S")

    # P0: sanitize client_name to prevent path traversal
    safe_client = re.sub(r'[^a-zA-Z0-9_\- ]', '', client_name)[:50].strip().lower().replace(' ', '-')
    if not safe_client:
        safe_client = "cliente"

    filename = f"soporte-{safe_client}-{report_id}.md"

    report = f"""# 🛠️ Reporte de Soporte Técnico

**Cliente:** {client_name}
**Fecha:** {timestamp}
**Reporte ID:** {report_id}

---

## 📋 Descripción del Problema

{issue_description}

---

## 🔍 Diagnóstico

{diagnosis}

---

## ✅ Solución Aplicada

{solution}

---

## 📝 Pasos Realizados

{steps_performed}

---

## 💡 Recomendaciones

{recommendations if recommendations else "Sin recomendaciones adicionales."}

---

*Reporte generado automáticamente por IT Support Auto-Pilot Agent.*
"""

    try:
        REPORTS_DIR.mkdir(parents=True, exist_ok=True)
        out_path = REPORTS_DIR / filename
        out_path.write_text(report, encoding="utf-8")
        return f"✅ Reporte guardado: {out_path}"
    except Exception as e:
        # P0: don't leak report content in error message
        return f"⚠️ Error guardando reporte: {e}"
