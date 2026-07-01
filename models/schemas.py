from __future__ import annotations

from dataclasses import dataclass


# Clase utilizada para representar el resultado de una skill (Product Owner, QA o Arquitectura).
# Debe definir los cuatro campos que TODA skill devuelve al terminar su trabajo.
@dataclass
class SkillResult:
    content: str
    is_mock: bool
    skill_name: str
    error: str | None = None


# Clase utilizada para representar el informe final del pipeline completo.
# Debe agrupar el requerimiento original y los cuatro resultados de las skills en un solo objeto.
@dataclass
class PipelineResult:
    requirement: str
    user_story: SkillResult
    qa_cases: SkillResult
    architecture: SkillResult
    security: SkillResult | None = None


