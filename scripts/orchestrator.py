from pathlib import Path
import subprocess
import sys

PROJECT_ROOT = Path(__file__).resolve().parent.parent
SCRIPTS_DIR = PROJECT_ROOT / "scripts"


def run_script(script_name: str) -> None:
    script_path = SCRIPTS_DIR / script_name

    if not script_path.is_file():
        raise f"Script {script_name} não encontrado"

    print(f"\n{'=' * 50}")
    print(f"Executando script: {script_name}")
    print(f"{'=' * 50}")

    subprocess.run(
        [sys.executable, str(script_path)],
        cwd=PROJECT_ROOT,
        check=True,
        timeout=300
    )


def run_tests() -> None:
    print("\n===== EXECUTANDO TESTES ALTOMATIZADOS =====")

    subprocess.run(
        [
            sys.executable,
            "-m",
            "pytest",
            "--cov=src",
            "--cov-branch",
            "--cov-report=term-missing",
            "--cov-fail-under=100"
        ],
        cwd=PROJECT_ROOT,
        check=True,
        timeout=600
    )


def main() -> int:
    print("\n===== AI DATA OPERATIONS =====")
    print("1 - Deploy")
    print("2 - Destroy")
    print("0 - Sair")

    choise = input("\nEscolha uma opção: ").strip()

    try:
        if choise == "1":
            run_tests()
            run_script("package_lambda.py")
            run_script("deploy.py")
        elif choise == "2":
            run_script("destroy.py")
        elif choise == "0":
            print("Operacao cancelada...")
            return 0
        else:
            print("Opção inválida. Tente novamente.")
            return 1

        print(f"\nPipeline de deploy finalizado.")
        return 0
    except subprocess.CalledProcessError as e:
        print(
            f"\nErro ao executar script. "
            f"Código de saída: {e.returncode}"
        )
        return e.returncode or 1
    except subprocess.TimeoutExpired as e:
        print(f"\nTIMEOUT: Operacao interrompida: {e}")
        return 124
    except (FileNotFoundError, KeyboardInterrupt) as e:
        print(f"\nOperacao interrompida: {e}")
        return 130 if isinstance(e, KeyboardInterrupt) else 1


if __name__ == "__main__":
    raise SystemExit(main())
