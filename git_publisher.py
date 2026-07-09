import subprocess
import logging
from pathlib import Path
from datetime import datetime

logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)s: %(message)s"
)


def executar(comando, pasta):
    """Executa um comando Git."""

    resultado = subprocess.run(
        comando,
        cwd=pasta,
        capture_output=True,
        text=True
    )

    if resultado.returncode != 0:
        raise RuntimeError(resultado.stderr.strip())

    return resultado.stdout.strip()


def localizar_repositorio():
    """
    Localiza automaticamente a pasta que contém o .git
    """

    pasta = Path(__file__).resolve().parent

    while pasta != pasta.parent:

        if (pasta / ".git").exists():
            return pasta

        pasta = pasta.parent

    raise RuntimeError("Repositório Git não encontrado.")


def publicar_git():

    repo = localizar_repositorio()

    logging.info(f"Repositório encontrado em:\n{repo}")

    # Adiciona arquivos
    executar(["git", "add", "."], repo)

    # Verifica se existe alteração
    status = executar(["git", "status", "--porcelain"], repo)

    if not status:
        return "Nenhuma alteração encontrada."

    mensagem = datetime.now().strftime(
        "Atualização automática %d/%m/%Y %H:%M"
    )

    executar(["git", "commit", "-m", mensagem], repo)

    executar(["git", "push", "origin", "main"], repo)

    return "Publicação realizada com sucesso!"


if __name__ == "__main__":

    try:

        print(publicar_git())

    except Exception as erro:

        print("ERRO:", erro)