from pathlib import Path
import subprocess
from command_runner import run_command

PROJECT_ROOT = Path(__file__).resolve().parent.parent
TERRAFORM_DIR = PROJECT_ROOT / "infrastructure" / "terraform"
VARIABLES_FILE = TERRAFORM_DIR / "environments" / "dev" /"terraform.tfvars"
PLAN_FILE = TERRAFORM_DIR / "terraform.tfplan"


def run(command: list[str]) -> None:
    print(f"\n>>> {' '.join(command)}")
    subprocess.run(command, cwd=TERRAFORM_DIR, check=True)


def destroy() -> None:
    if not VARIABLES_FILE.is_file():
        raise FileNotFoundError(f"Arquivo de variáveis {VARIABLES_FILE} não encontrado")

    print("\nATENCAO: voce escolheu DESTROY.")
    print("Os recursos gerenciados por este estado podem ser removidos.")

    run_command(["terraform", "init", "-input=false"], TERRAFORM_DIR)
    run_command(["terraform", "validate"], TERRAFORM_DIR)
    run_command([
        "terraform",
        "plan",
        "-destroy",
        "-input=false",
        f"-var-file={VARIABLES_FILE}",
        f"-out={PLAN_FILE}"
    ],
        TERRAFORM_DIR
    )

    confirmation = input("\nRevise o plano. Deseja aplicar O DESTROY? Digite 'DESTROY': ").strip().upper()

    if confirmation != "DESTROY":
        print("Destroy cancelado.")
        return

    run_command(["terraform", "apply", "-input=false", str(PLAN_FILE)], TERRAFORM_DIR)

    print("\nDestroy concluído com sucesso.")


if __name__ == "__main__":
    try:
        destroy()
    except subprocess.CalledProcessError as error:
        print(f"\nErro ao executar script. Código de saída: {error.returncode}")
        raise SystemExit(error.returncode or 1)
    except KeyboardInterrupt:
        print("\nOperacao interrompida.")
        raise SystemExit(130)
    except FileNotFoundError as error:
        print(f"\nErro ao executar script: {error}")
        raise SystemExit(1)
