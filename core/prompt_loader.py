from __future__ import annotations

from pathlib import Path


# Clase de excepción utilizada cuando no se encuentra un archivo de prompt.
# Debe heredar de Exception para que las skills puedan capturarla y usar un prompt de respaldo.
class PromptNotFoundError(Exception):
    pass


class PromptLoader:
    # Método utilizado para inicializar el cargador de prompts y resolver la ruta a la carpeta prompts/.
    # Debe guardar la ruta en self.prompts_dir como un objeto Path.
    def __init__(self, prompts_dir: str | Path | None = None) -> None:
        if prompts_dir is not None:
            self.prompts_dir = Path(prompts_dir)
        else:
            self.prompts_dir = Path(__file__).resolve().parent.parent / "prompts"

    # Método utilizado para leer el contenido completo de un archivo de prompt.
    # Debe construir la ruta completa, verificar que exista y leer el archivo.
    def load(self, prompt_filename: str) -> str:
        path = self.prompts_dir / prompt_filename
        if not path.exists():
            raise PromptNotFoundError(
                f"Prompt file not found: {prompt_filename}"
            )
        return path.read_text(encoding="utf-8")
