from models.schemas import PipelineResult, SkillResult


class MarkdownFormatter:
    # Método estático utilizado para convertir un SkillResult en un bloque Markdown con encabezado.
    # Debe manejar error, banner de mock y contenido; retornar str para st.markdown().
    @staticmethod
    def format_skill_result(result: SkillResult, title: str) -> str:
        lines = [f"## {title}", ""]

        if result.error is not None:
            lines.append(f"> Error: {result.error}")
            return "\n".join(lines)

        if result.is_mock:
            lines.append("> Generado en modo mock.")
            lines.append("")

        lines.append(result.content)
        return "\n".join(lines)

    # Método estático utilizado para formatear el PipelineResult completo (las cuatro secciones juntas).
    # Debe llamar format_skill_result cuatro veces, una por cada skill del pipeline si está presente.
    @staticmethod
    def format_pipeline_result(pipeline_result: PipelineResult) -> str:
        sections = [
            MarkdownFormatter.format_skill_result(
                pipeline_result.user_story, "Historia de Usuario"
            ),
            MarkdownFormatter.format_skill_result(
                pipeline_result.qa_cases, "Casos de Prueba"
            ),
            MarkdownFormatter.format_skill_result(
                pipeline_result.architecture, "Recomendacion Arquitectonica"
            ),
        ]
        if pipeline_result.security is not None:
            sections.append(
                MarkdownFormatter.format_skill_result(
                    pipeline_result.security, "Seguridad y CI/CD"
                )
            )
        return "\n\n---\n\n".join(sections)


