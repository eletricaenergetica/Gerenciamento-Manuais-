# database.py
import sqlite3
import os
import logging
from pathlib import Path
from typing import List, Tuple, Optional

logger = logging.getLogger(__name__)
# configure logging básico apenas se não houver configuração externa
if not logging.getLogger().handlers:
    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")

# Nome do arquivo DB — use caminho absoluto relativo a este módulo para evitar problemas de cwd
DB_NAME = "manuais.db"
DB_PATH = str(Path(__file__).parent.resolve() / DB_NAME)


def conectar():
    """Conecta ao banco no caminho DB_PATH."""
    logger.debug("Conectando ao DB em: %s", DB_PATH)
    return sqlite3.connect(DB_PATH)


def criar_tabela():
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS manuais (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        projeto TEXT,
        nome TEXT,
        caminho TEXT
    )
    """)

    conn.commit()
    conn.close()


def inserir_manual(projeto, nome, caminho):
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO manuais (projeto, nome, caminho)
    VALUES (?, ?, ?)
    """, (projeto.strip(), nome, caminho))

    conn.commit()
    conn.close()


def listar_manuais(projeto=None) -> List[Tuple]:
    """
    Retorna lista de tuplas (id, nome, caminho).
    Se projeto for fornecido, faz comparação case-insensitive.
    """
    logger.info("Listando manuais para projeto: %r (DB: %s)", projeto, DB_PATH)
    conn = conectar()
    cursor = conn.cursor()

    if projeto:
        cursor.execute("""
        SELECT id, nome, caminho 
        FROM manuais 
        WHERE LOWER(projeto)=LOWER(?)
        """, (projeto.strip(),))
    else:
        cursor.execute("""
        SELECT id, nome, caminho 
        FROM manuais
        """)

    dados = cursor.fetchall()
    conn.close()
    logger.info("Registros retornados: %d", len(dados))
    return dados


def deletar_manual(id_manual):
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM manuais WHERE id=?", (id_manual,))

    conn.commit()
    conn.close()


# Funções extras úteis para depurar/inspecionar
def listar_projetos() -> List[str]:
    """Retorna a lista de projetos distintos registrados no DB."""
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT DISTINCT projeto FROM manuais")
    rows = cursor.fetchall()
    conn.close()
    return [r[0] for r in rows if r and r[0] is not None]


def buscar_projetos_like(padrao: str) -> List[str]:
    """Procura projetos que contenham o padrão (case-insensitive)."""
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT DISTINCT projeto FROM manuais WHERE projeto LIKE ?", (f"%{padrao}%",))
    rows = cursor.fetchall()
    conn.close()
    return [r[0] for r in rows if r and r[0] is not None]


# debug rápido quando executado diretamente
if __name__ == "__main__":
    print("DB_PATH =", DB_PATH)
    criar_tabela()
    print("Projetos cadastrados:", listar_projetos())
    print("Exemplos de registros (até 20):")
    conn = conectar()
    cur = conn.cursor()
    cur.execute("SELECT id, projeto, nome, caminho FROM manuais LIMIT 20")
    for row in cur.fetchall():
        print(row)
    conn.close()