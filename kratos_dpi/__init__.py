# inject to kratos' namespace
import kratos
from .func import dpi_python
from .compile import dpi_compile

__all__ = ["dpi_python", "dpi_compile"]
