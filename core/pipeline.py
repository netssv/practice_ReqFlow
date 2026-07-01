from models.schemas import PipelineResult
from skills.architecture_skill import ArchitectureSkill
from skills.product_owner_skill import ProductOwnerSkill
from skills.qa_skill import QASkill
from skills.security_skill import SecuritySkill


class RequirementPipeline:
    # Método utilizado para inicializar el pipeline con las cuatro skills.
    # Debe guardar cada skill en un atributo; usar instancias por defecto si se recibe None.
    def __init__(
        self,
        product_owner_skill: ProductOwnerSkill | None = None,
        qa_skill: QASkill | None = None,
        architecture_skill: ArchitectureSkill | None = None,
        security_skill: SecuritySkill | None = None,
    ) -> None:
        self.product_owner_skill = product_owner_skill or ProductOwnerSkill()
        self.qa_skill = qa_skill or QASkill()
        self.architecture_skill = architecture_skill or ArchitectureSkill()
        self.security_skill = security_skill or SecuritySkill()

    # Método utilizado para ejecutar el pipeline completo sobre un requerimiento de texto.
    # Debe llamar PO → QA → Arquitectura → Seguridad acumulando context y retornar PipelineResult.
    def execute(self, requirement: str) -> PipelineResult:
        user_story_result = self.product_owner_skill.run(requirement, context="")
        qa_result = self.qa_skill.run(requirement, context=user_story_result.content)
        
        combined_po_qa = f"{user_story_result.content}\n\n{qa_result.content}"
        architecture_result = self.architecture_skill.run(requirement, context=combined_po_qa)
        
        combined_all = f"{combined_po_qa}\n\n{architecture_result.content}"
        security_result = self.security_skill.run(requirement, context=combined_all)
        
        return PipelineResult(
            requirement=requirement,
            user_story=user_story_result,
            qa_cases=qa_result,
            architecture=architecture_result,
            security=security_result,
        )

