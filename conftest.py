import pytest
import kratos
import kratos_dpi


@pytest.fixture(autouse=True)
def clear_kratos_context():
    kratos.Generator.clear_context()
    kratos_dpi.clear_context()
