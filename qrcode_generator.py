import os
import qrcode


def gerar_qr(link, nome_saida="qrcode.png", pasta="qrcodes"):
    """
    Gera um QR Code apontando para um link (URL).
    """

    if not link:
        raise ValueError("Link inválido para geração do QR Code.")

    os.makedirs(pasta, exist_ok=True)

    # garante nome único por segurança (evita sobrescrever sem querer)
    if not nome_saida.endswith(".png"):
        nome_saida += ".png"

    caminho_saida = os.path.join(pasta, nome_saida)

    qr = qrcode.QRCode(
        version=None,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=10,
        border=4
    )

    qr.add_data(link)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")
    img.save(caminho_saida)

    return caminho_saida