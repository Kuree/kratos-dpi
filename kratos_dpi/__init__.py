# inject to kratos' namespace
import kratos
from .func import dpi_python, clear_context
from .compile import dpi_compile

__all__ = ["dpi_python", "dpi_compile", "clear_context"]
