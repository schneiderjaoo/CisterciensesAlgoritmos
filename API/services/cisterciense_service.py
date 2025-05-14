import cv2
import numpy as np
import os
from flask import Flask, send_from_directory, jsonify

app = Flask(__name__)

DIRETORIO_SIMBOLOS = os.path.join(os.getcwd(), "static", "symbols", "output")
DIRETORIO_OUTPUT = os.path.join(os.getcwd(), "static", "output")

if not os.path.exists(DIRETORIO_OUTPUT):
    os.makedirs(DIRETORIO_OUTPUT)

def carregar_imagem(numero):
    caminho = os.path.join(DIRETORIO_SIMBOLOS, f'{numero}.png')
    if os.path.exists(caminho):
        return cv2.imread(caminho, cv2.IMREAD_UNCHANGED)
    else:
        print(f"Imagem {numero}.png não encontrada!")
        return None

def criar_canvas():
    tamanho = 200
    return np.zeros((tamanho, tamanho, 4), dtype=np.uint8)

def sobrepor_imagem(base, img, cor_linhas=None):
    h, w = img.shape[:2]
    H, W = base.shape[:2]

    y_offset = (H - h) // 2
    x_offset = (W - w) // 2

    for y in range(h):
        for x in range(w):
            if y + y_offset < base.shape[0] and x + x_offset < base.shape[1]:
                alpha = img[y, x, 3] / 255.0
                if alpha > 0:
                    for c in range(3):
                        if cor_linhas is not None:
                            base[y + y_offset, x + x_offset, c] = cor_linhas[c]
                        else:
                            base[y + y_offset, x + x_offset, c] = (
                                alpha * img[y, x, c] + (1 - alpha) * base[y + y_offset, x + x_offset, c]
                            )
                    base[y + y_offset, x + x_offset, 3] = max(base[y + y_offset, x + x_offset, 3], img[y, x, 3])

def gerar_numero_cisterciense(numero):
    partes = {
        "unidades": (numero % 10),
        "dezenas": (numero // 10 % 10) * 10,
        "centenas": (numero // 100 % 10) * 100,
        "milhares": (numero // 1000 % 10) * 1000
    }

    canvas_final = criar_canvas()
    imagens_destacadas = []

    for valor in partes.values():
        if valor > 0:
            img = carregar_imagem(valor)
            if img is not None:
                sobrepor_imagem(canvas_final, img)

                canvas_aux = criar_canvas()
                sobrepor_imagem(canvas_aux, img, cor_linhas=(0, 0, 255)) 
                caminho_aux = os.path.join(DIRETORIO_OUTPUT, f"aux_{valor}.png")
                cv2.imwrite(caminho_aux, canvas_aux)
                imagens_destacadas.append(f"aux_{valor}.png")

    caminho_saida = os.path.join(DIRETORIO_OUTPUT, "numero_gerado.png")
    cv2.imwrite(caminho_saida, canvas_final)

    return caminho_saida, imagens_destacadas

@app.route("/gerar/<int:numero>")
def gerar(numero):
    try:
        caminho_imagem, imagens_aux = gerar_numero_cisterciense(numero)
        return jsonify({
            "imagem_principal": "numero_gerado.png",
            "imagens_auxiliares": imagens_aux
        })
    except Exception as e:
        return jsonify({"erro": str(e)}), 500

@app.route("/imagem/<nome>")
def obter_imagem(nome):
    return send_from_directory(DIRETORIO_OUTPUT, nome)

if __name__ == "__main__":
    app.run(debug=True)
