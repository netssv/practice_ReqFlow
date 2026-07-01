from __future__ import annotations

from typing import Literal

import streamlit as st

from core.ai_proxy_client import AIProxyClient
from models.schemas import PipelineResult, SkillResult
from utils.formatter import MarkdownFormatter

BadgeStatus = Literal["success", "warning", "error"]

SKILL_TABS = (
    {
        "key": "user_story",
        "label": "📋 Historia de Usuario",
        "title": "Historia de Usuario",
        "accent": "#1E88E5",
    },
    {
        "key": "qa_cases",
        "label": "✅ Casos de Prueba",
        "title": "Casos de Prueba",
        "accent": "#00897B",
    },
    {
        "key": "architecture",
        "label": "🏗️ Recomendacion Arquitectonica",
        "title": "Recomendacion Arquitectonica",
        "accent": "#5E35B1",
    },
    {
        "key": "security",
        "label": "🛡️ Seguridad y CI/CD",
        "title": "Seguridad y CI/CD",
        "accent": "#E53935",
    },
)


def badge_status(result: SkillResult) -> BadgeStatus:
    if result.error:
        return "error"
    if result.is_mock:
        return "warning"
    return "success"


def badge_label(result: SkillResult) -> str:
    status = badge_status(result)
    if status == "error":
        return "Error en generacion"
    if status == "warning":
        return "Modo mock"
    return "Generado con IA"


def inject_theme_css() -> None:
    st.markdown(
        """
        <style>
        /* Estilos generales responsivos */
        html, body, [class*="css"] {
            font-size: 15px;
        }
        
        .reqflow-hero {
            padding: 1rem 1.25rem;
            border-radius: 0.75rem;
            margin-bottom: 1rem;
            background: linear-gradient(
                135deg,
                rgba(30, 136, 229, 0.12) 0%,
                rgba(94, 53, 177, 0.12) 100%
            );
            border: 1px solid rgba(30, 136, 229, 0.25);
        }
        .reqflow-hero h1 {
            margin: 0;
            font-size: 1.75rem;
            font-weight: 700;
        }
        .reqflow-hero p {
            margin: 0.35rem 0 0;
            opacity: 0.85;
            font-size: 0.95rem;
            line-height: 1.3;
        }
        .reqflow-card-accent {
            border-top: 4px solid var(--reqflow-accent);
            border-radius: 0.5rem;
            padding-top: 0.15rem;
        }

        /* Optimización específica para móviles */
        @media (max-width: 640px) {
            .reqflow-hero h1 {
                font-size: 1.5rem;
            }
            .reqflow-hero p {
                font-size: 0.85rem;
            }
            div[data-testid="column"] {
                min-width: 100% !important;
                margin-bottom: 0.5rem;
            }
            .stTabs [data-baseweb="tab-list"] {
                flex-wrap: wrap;
                gap: 5px;
            }
            .stTabs button {
                padding: 8px 12px !important;
                font-size: 13px !important;
            }
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def render_header() -> None:
    st.markdown(
        """
        <div class="reqflow-hero">
            <h1>🧩 ReqFlow</h1>
            <p>Convierte un requerimiento en historia de usuario, casos de prueba y recomendacion arquitectonica.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_proxy_status(ai_client: AIProxyClient) -> None:
    with st.sidebar:
        st.header("Estado del API")
        if ai_client.is_available:
            provider_name = getattr(ai_client, "provider", "proxy").upper()
            model_name = getattr(ai_client, "model", "Desconocido")
            st.success(f"IA Conectada ({provider_name})")
            st.info(f"**Modelo activo:**\n`{model_name}`")
        else:
            st.warning("Modo Mock (Sin IA)")
            st.caption(
                "Configura las variables de entorno en el archivo `.env` para usar IA real."
            )

        st.divider()
        st.subheader("Pipeline")
        st.markdown(
            "1. **Product Owner** — historia de usuario\n"
            "2. **QA** — casos de prueba\n"
            "3. **Arquitectura** — recomendacion tecnica\n"
            "4. **Seguridad** — seguridad y CI/CD"
        )


def render_skill_badge(result: SkillResult) -> None:
    status = badge_status(result)
    label = badge_label(result)
    if status == "error":
        st.error(label)
    elif status == "warning":
        st.warning(label)
    else:
        st.success(label)


def render_skill_tab(result: SkillResult, title: str, accent: str) -> None:
    st.markdown(
        f'<div class="reqflow-card-accent" style="--reqflow-accent: {accent};"></div>',
        unsafe_allow_html=True,
    )
    with st.container(border=True):
        render_skill_badge(result)
        st.markdown(
            MarkdownFormatter.format_skill_result(result, title),
            unsafe_allow_html=False,
        )


def render_metrics_row(pipeline_result: PipelineResult) -> None:
    results = [
        pipeline_result.user_story,
        pipeline_result.qa_cases,
        pipeline_result.architecture,
    ]
    labels = ["PO", "QA", "Arquitectura"]
    if pipeline_result.security is not None:
        results.append(pipeline_result.security)
        labels.append("Seguridad")
        
    columns = st.columns(len(results))
    for column, label, result in zip(columns, labels, results, strict=True):
        with column:
            st.metric(label=label, value=badge_label(result))


def render_results_tabs(pipeline_result: PipelineResult) -> None:
    tabs_config = list(SKILL_TABS)
    if pipeline_result.security is None:
        # Filtrar si no hay seguridad
        tabs_config = [t for t in tabs_config if t["key"] != "security"]
        
    tab_labels = [tab["label"] for tab in tabs_config]
    tabs = st.tabs(tab_labels)

    for tab, config in zip(tabs, tabs_config, strict=True):
        with tab:
            result = getattr(pipeline_result, config["key"])
            render_skill_tab(result, config["title"], config["accent"])


    st.divider()
    export_content = MarkdownFormatter.format_pipeline_result(pipeline_result)
    st.download_button(
        label="Descargar artefactos (.md)",
        data=export_content,
        file_name="reqflow-artefactos.md",
        mime="text/markdown",
    )

