import subprocess
from pathlib import Path

TIMEOUT_SECONDS = 300


def run_command(command: list[str], cwd: Path, timeout: int = TIMEOUT_SECONDS) -> None:
    print(f"\n>>> {' '.join(command)}", flush=True)
    print(f"Timeout: {timeout} segundos", flush=True)

    try:
        subprocess.run(command, cwd=cwd, check=True, timeout=timeout)
    except subprocess.TimeoutExpired:
        raise TimeoutError(
            f"Comando excedeu o limite de {timeout} segundos: "
            f"{command[0]}"
        ) from None
