import os
import shutil
import logging
import sys

import database as db
import html_generator as htmlg


# 🔥 URL DO SEU GITHUB PAGES (AJUSTADO)
GITHUB_BASE_URL = "https://eletricaenergetica.github.io/Gerenciamento-Manuais"

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")


def _extrair_origem(manual):
    """Tenta extrair o caminho do PDF de um registro `manual`."""
    if isinstance(manual, dict):
        for key in ("origem", "path", "arquivo", "caminho", "file", "filepath"):
            if key in manual and manual[key]:
                return manual[key]
    elif isinstance(manual, (list, tuple)):
        # tenta a posição 2 (como no código original), depois último item
        if len(manual) >= 3 and manual[2]:
            return manual[2]
        if len(manual) >= 1 and manual[-1]:
            return manual[-1]
    return None


def gerar_site(projeto):
    dados = db.listar_manuais(projeto) or []

    if not dados:
        raise RuntimeError("Nenhum manual encontrado para este projeto.")

    site_dir = "site"
    projeto_pdf_dir = os.path.join(site_dir, "pdfs", projeto)

    # Remove site antigo
    if os.path.exists(site_dir):
        logging.info("Removendo diretório antigo: %s", site_dir)
        shutil.rmtree(site_dir)

    # Recria estrutura
    os.makedirs(projeto_pdf_dir, exist_ok=True)

    # Copia PDFs (preservando nome do arquivo)
    for manual in dados:
        origem = None
        try:
            origem = _extrair_origem(manual)
        except Exception:
            logging.warning("Falha ao extrair caminho do manual: %r", manual)
            continue

        if not origem:
            logging.warning("Caminho do PDF não encontrado no registro: %r", manual)
            continue

        if os.path.exists(origem):
            nome_arquivo = os.path.basename(origem)
            destino = os.path.join(projeto_pdf_dir, nome_arquivo)
            try:
                shutil.copy2(origem, destino)
                logging.info("Copiado: %s -> %s", origem, destino)
            except Exception as e:
                logging.warning("Erro ao copiar %s: %s", origem, e)
        else:
            logging.warning("Arquivo não encontrado: %s", origem)

    # Gera HTML (assume-se que htmlg.gerar_html retorna o caminho do HTML gerado)
    html_path = htmlg.gerar_html(projeto, dados, pasta_saida=site_dir)

    # Link público GitHub Pages
    link = f"{GITHUB_BASE_URL}/{projeto}.html"

    return html_path, link


if __name__ == "__main__":
    try:
        html_path, link = gerar_site("Manuais")
        print("HTML gerado:", html_path)
        print("Link público:", link)
    except Exception:
        logging.exception("Erro ao gerar site")
        sys.exit(1)