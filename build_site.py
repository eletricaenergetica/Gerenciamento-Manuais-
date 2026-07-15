import os
import shutil
import logging
import sys

import database as db
import html_generator as htmlg


# URL DO SEU GITHUB PAGES
GITHUB_BASE_URL = "https://eletricaenergetica.github.io/Gerenciamento-Manuais"


logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)s: %(message)s"
)


def _extrair_origem(manual):
    """
    Extrai o caminho do PDF do registro do banco.
    """
    if isinstance(manual, dict):
        for key in (
            "origem",
            "path",
            "arquivo",
            "caminho",
            "file",
            "filepath"
        ):
            if key in manual and manual[key]:
                return manual[key]

    elif isinstance(manual, (list, tuple)):
        if len(manual) >= 3 and manual[2]:
            return manual[2]

        if len(manual) >= 1 and manual[-1]:
            return manual[-1]

    return None


def gerar_site(projeto):
    dados = db.listar_manuais(projeto) or []

    if not dados:
        raise RuntimeError(
            "Nenhum manual encontrado para este projeto."
        )

    site_dir = "."
    projeto_pdf_dir = os.path.join(
        "pdfs",
        projeto
    )

    # Remove pastas antigas de distribuição para gerar do zero
    if os.path.exists("pdfs"):
        logging.info("Removendo pasta antiga de distribuição: pdfs")
        shutil.rmtree("pdfs")

    if os.path.exists("index.html"):
        logging.info("Removendo index.html antigo")
        os.remove("index.html")

    # Cria estrutura nova de distribuição
    os.makedirs(
        projeto_pdf_dir,
        exist_ok=True
    )

    # Copia PDFs
    for manual in dados:
        origem = _extrair_origem(manual)

        if not origem:
            logging.warning(
                "PDF sem caminho: %s",
                manual
            )
            continue

        nome_arquivo = os.path.basename(origem)
        destino = os.path.join(
            projeto_pdf_dir,
            nome_arquivo
        )

        # Caminho alternativo na nossa pasta local segura
        caminho_local_seguro = os.path.join("manuais_originais", nome_arquivo)

        # Se o caminho original do banco não existir, tenta pegar da nossa pasta manuais_originais
        if not os.path.exists(origem) and os.path.exists(caminho_local_seguro):
            origem = caminho_local_seguro

        if os.path.exists(origem):
            shutil.copy2(
                origem,
                destino
            )

            logging.info(
                "Copiado com sucesso: %s -> %s",
                origem,
                destino
            )
        else:
            logging.warning(
                "Arquivo não encontrado em 'manuais_originais': %s",
                nome_arquivo
            )

    # Gera HTML
    html_path = htmlg.gerar_html(
        projeto,
        dados,
        pasta_saida=site_dir
    )

    # Link público GitHub Pages
    link = GITHUB_BASE_URL

    return html_path, link


if __name__ == "__main__":
    try:
        html_path, link = gerar_site(
            "Gerenciamento-Manuais"
        )

        print(
            "HTML gerado:",
            html_path
        )

        print(
            "Link público:",
            link
        )

    except Exception:
        logging.exception(
            "Erro ao gerar site"
        )
        sys.exit(1)