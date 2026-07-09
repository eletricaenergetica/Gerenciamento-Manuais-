import os
import html


def gerar_html(projeto, lista_pdfs, pasta_saida="site"):

    # segurança: evita erro se não tiver PDFs
    if not lista_pdfs:
        raise Exception("Nenhum manual encontrado para gerar o HTML.")

    os.makedirs(pasta_saida, exist_ok=True)

    caminho_html = os.path.join(pasta_saida, f"{projeto}.html")

    lista_pdfs = sorted(lista_pdfs, key=lambda x: x[1].lower())

    html_content = f"""<!DOCTYPE html>
<html lang="pt-BR">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{html.escape(projeto)}</title>

    <style>
        body {{
            font-family: Arial, Helvetica, sans-serif;
            background:#1e1e1e;
            color:white;
            text-align:center;
            margin:0;
            padding:30px;
        }}

        h1 {{
            color:#00BFFF;
        }}

        .card{{
            background:#2d2d2d;
            width:340px;
            margin:15px auto;
            padding:18px;
            border-radius:12px;
            box-shadow:0 0 8px rgba(0,0,0,.3);
        }}

        a{{
            display:block;
            margin-top:15px;
            padding:10px;
            background:#0d6efd;
            color:white;
            text-decoration:none;
            border-radius:8px;
        }}

        a:hover{{
            background:#0b5ed7;
        }}
    </style>

</head>

<body>

<h1>📚 {html.escape(projeto)}</h1>

<h3>{len(lista_pdfs)} Manual(is) disponível(is)</h3>
"""

    for pdf in lista_pdfs:

        nome = html.escape(pdf[1])
        arquivo_pdf = os.path.basename(pdf[2])

        # caminho compatível com GitHub Pages
        link_pdf = f"pdfs/{projeto}/{arquivo_pdf}"

        html_content += f"""
<div class="card">

<h3>📄 {nome}</h3>

<a href="{link_pdf}" target="_blank">
Abrir Manual
</a>

</div>
"""

    html_content += """
</body>
</html>
"""

    with open(caminho_html, "w", encoding="utf-8") as f:
        f.write(html_content)

    return caminho_html