from core.ai_proxy_client import AIProxyClient
from core.prompt_loader import PromptLoader
from models.schemas import SkillResult
from skills.base_skill import BaseSkill


class ProductOwnerSkill(BaseSkill):
    # Método utilizado para configurar la skill de Product Owner con su nombre y archivo de prompt.
    # Debe llamar a super().__init__() con skill_name="product_owner" y prompt_filename="product_owner.md".
    def __init__(
        self,
        ai_client: AIProxyClient | None = None,
        prompt_loader: PromptLoader | None = None,
    ) -> None:
        super().__init__(
            skill_name="product_owner",
            prompt_filename="product_owner.md",
            ai_client=ai_client,
            prompt_loader=prompt_loader,
        )

    # Método utilizado para devolver una respuesta de ejemplo cuando no hay IA disponible o falla el proxy.
    # Debe retornar SkillResult con historia de usuario en Markdown e is_mock=True.
    def _mock_response(self, requirement: str) -> SkillResult:
        content = (
            "### Historia de Usuario\n\n"
            f"**Como** usuario del sistema,\n"
            f"**quiero** {requirement},\n"
            "**para** mejorar mi experiencia y cumplir con el objetivo del negocio.\n\n"
            "### Criterios de Aceptacion\n\n"
            "- El sistema implementa la funcionalidad descrita en el requerimiento.\n"
            "- La interfaz es clara y accesible para el usuario final.\n"
            "- Se manejan los casos de error con mensajes descriptivos."
        )
        return SkillResult(
            content=content,
            is_mock=True,
            skill_name=self.skill_name,
            error=None,
        )
