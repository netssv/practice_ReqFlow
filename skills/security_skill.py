from core.ai_proxy_client import AIProxyClient
from core.prompt_loader import PromptLoader
from models.schemas import SkillResult
from skills.base_skill import BaseSkill


class SecuritySkill(BaseSkill):
    def __init__(
        self,
        ai_client: AIProxyClient | None = None,
        prompt_loader: PromptLoader | None = None,
    ) -> None:
        super().__init__(
            skill_name="security",
            prompt_filename="security.md",
            ai_client=ai_client,
            prompt_loader=prompt_loader,
        )

    def _mock_response(self, requirement: str) -> SkillResult:
        content = (
            "### Recomendaciones de Seguridad y CI/CD\n\n"
            f"Análisis para el requerimiento: '{requirement}':\n\n"
            "#### 1. Riesgos de Seguridad Detectados\n"
            "- Fuga de credenciales o API keys en código duro.\n"
            "- Falta de validación y sanitización en entradas del usuario.\n"
            "- Exposición involuntaria de endpoints internos.\n\n"
            "#### 2. Controles Sugeridos\n"
            "- **Manejo de Secretos:** Utilizar variables de entorno y Secret Managers en nube.\n"
            "- **Validación estricta:** Implementar esquemas de validación de datos (ej: Pydantic).\n"
            "- **Autenticación segura:** Validar tokens mediante flujos OAuth2 oficiales.\n\n"
            "#### 3. Pipeline de Integración Continua (CI/CD)\n"
            "- **Linter:** Ejecutar `ruff` o `flake8` para análisis estático.\n"
            "- **SAST:** Pasar escáner `bandit` para buscar vulnerabilidades en código Python.\n"
            "- **Pruebas:** Correr `pytest` en cada Pull Request antes de fusionar."
        )
        return SkillResult(
            content=content,
            is_mock=True,
            skill_name=self.skill_name,
            error=None,
        )
