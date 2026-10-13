from pathlib import Path
import subprocess
from command_runner import run_command

PROJECT_ROOT = Path(__file__).resolve().parent.parent
TERRAFORM_DIR = PROJECT_ROOT / "infrastructure" / "terraform"
VARIABLES_FILE = TERRAFORM_DIR / "environments" / "dev" /"terraform.tfvars"


def deploy() -> None:
    if not VARIABLES_FILE.is_file():
        raise FileNotFoundError(f"Arquivo de variáveis {VARIABLES_FILE} não encontrado")

    run_command(["terraform", "init", "-input=false"], TERRAFORM_DIR)
    run_command(["terraform", "fmt", "-recursive"], TERRAFORM_DIR)
    run_command(["terraform", "validate"], TERRAFORM_DIR)
    run_command([
        "terraform",
        "plan",
        "-input=false",
        f"-var-file={VARIABLES_FILE}",
        "-out=terraform.tfplan"
    ], TERRAFORM_DIR)

    confirmation = input("\nRevise o plano. Deseja aplicar? Digite 'sim': ").strip().lower()

    if confirmation != "sim":
        print("Deploy cancelado.")
        return

    run_command(["terraform", "apply", "-input=false", "terraform.tfplan"], TERRAFORM_DIR)

    print("\nDeploy concluído com sucesso.")


if __name__ == "__main__":
    deploy()

