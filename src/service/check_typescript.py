import subprocess
import tempfile
import os
from src.api.core.decorators.service_error_handler import service_error_handler
@service_error_handler(module="check.typescript.error")
def check_typescript(imports: str, code: str):
    """
    Compila (sin emitir) un archivo TS y lanza Exception si hay errores.
    """
    with tempfile.TemporaryDirectory() as tmpdir:
        ts_path = os.path.join(tmpdir, "solution.ts")
        # Escribe imports + código en el archivo
        with open(ts_path, "w", encoding="utf-8") as f:
            f.write(imports + "\n\n" + code)
        # Invoca `tsc` sin generar salida (--noEmit)
        result = subprocess.run(
            ["tsc", "--noEmit", ts_path],
            capture_output=True,
            text=True,
        )
        if result.returncode != 0:
            # Error de compilación de TS
            raise Exception(result.stderr.strip())