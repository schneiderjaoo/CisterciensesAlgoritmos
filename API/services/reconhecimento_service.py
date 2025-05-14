import cv2
import numpy as np
import os
import sys
import itertools
from skimage.metrics import structural_similarity as ssim

DIRETORIO_SIMBOLOS = r'C:\Estudos\Algoritmos Avançados - Martim\AlgoritmoCistercienses\API\static\symbols\output'
TAMANHO_DESEJADO = (93, 133)


def carregar_simbolos(tamanho=(128, 128)):
    simbolos = {}
    for valor in [
        1,2,3,4,5,6,7,8,9,
        10,20,30,40,50,60,70,80,90,
        100,200,300,400,500,600,700,800,900,
        1000,2000,3000,4000,5000,6000,7000,8000,9000
    ]:
        caminho = os.path.join(DIRETORIO_SIMBOLOS, f"{valor}.png")
        if os.path.exists(caminho):
            img = carregar_e_processar_imagem(caminho, tamanho)
            simbolos[valor] = img
    return simbolos

def carregar_e_processar_imagem(caminho_imagem, tamanho=(128, 128)):
    img = cv2.imread(caminho_imagem, cv2.IMREAD_UNCHANGED)

    if img is None:
        raise FileNotFoundError(f"Imagem não encontrada: {caminho_imagem}")

    if img.shape[-1] == 4:
        alpha_channel = img[:, :, 3]
        rgb_channels = img[:, :, :3]
        white_background = np.ones_like(rgb_channels, dtype=np.uint8) * 255
        alpha_factor = alpha_channel[:, :, np.newaxis] / 255.0
        img_rgb = rgb_channels * alpha_factor + white_background * (1 - alpha_factor)
        img = img_rgb.astype(np.uint8)

    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    media_brilho = np.mean(img_gray)

    if media_brilho > 127:
        _, img_bin = cv2.threshold(img_gray, 127, 255, cv2.THRESH_BINARY_INV)
    else:
        _, img_bin = cv2.threshold(img_gray, 127, 255, cv2.THRESH_BINARY)

    img_resized = cv2.resize(img_bin, tamanho, interpolation=cv2.INTER_NEAREST)
    return img_resized

def imagem_esta_no_padrao_correto(img_gray, limiar=127):
    """
    Retorna True se a imagem estiver no padrão: símbolo branco em fundo preto.
    """
    _, img_bin = cv2.threshold(img_gray, limiar, 255, cv2.THRESH_BINARY)
    proporcao_fundo_branco = np.sum(img_bin == 255) / img_bin.size
    return proporcao_fundo_branco < 0.5  

def imagens_semelhantes(img1, img2):
    return ssim(img1, img2)

def gerar_todas_composicoes_possiveis(simbolos, max_combinacoes=4):
    composicoes = {}
    valores = list(simbolos.keys())

    for r in range(2, max_combinacoes + 1):  
        for combinacao in itertools.combinations(valores, r):
            soma_valor = sum(combinacao)
            if soma_valor in simbolos or soma_valor in composicoes:
                continue

            img_combinada = simbolos[combinacao[0]]
            for val in combinacao[1:]:
                img_combinada = cv2.bitwise_or(img_combinada, simbolos[val])
            
            composicoes[soma_valor] = img_combinada

    return composicoes

def combinar_simbolos(simbolos):
    composicoes = {}
    valores = list(simbolos.keys())

    for i in range(len(valores)):
        for j in range(i + 1, len(valores)):
            val1, val2 = valores[i], valores[j]
            soma_valor = val1 + val2
            if soma_valor in simbolos:
                continue
            img1 = simbolos[val1]
            img2 = simbolos[val2]
            combinada = cv2.bitwise_or(img1, img2)
            composicoes[soma_valor] = combinada

    return composicoes

def reconhecer_numero(caminho_imagem, tamanho=(128, 128), verbose=True):
    imagem_input = carregar_e_processar_imagem(caminho_imagem, tamanho)

    nome_base = os.path.splitext(os.path.basename(caminho_imagem))[0]
    nome_saida = f"{nome_base}_processada.png"
    cv2.imwrite(nome_saida, imagem_input)
    print(f"Imagem processada salva como: {nome_saida}")

    simbolos = carregar_simbolos(tamanho)
    melhor_score = 0
    melhor_valor = None

    for valor, simbolo_img in simbolos.items():
        score = imagens_semelhantes(imagem_input, simbolo_img)
        if verbose:
            print(f"Score com {valor}: {score:.4f}")
        if score > melhor_score:
            melhor_score = score
            melhor_valor = valor

    composicoes = gerar_todas_composicoes_possiveis(simbolos)

    for valor_combinado, img_combinada in composicoes.items():
        score = imagens_semelhantes(imagem_input, img_combinada)
        if verbose:
            print(f"Score com composição {valor_combinado}: {score:.4f}")
        if score > melhor_score:
            melhor_score = score
            melhor_valor = valor_combinado

    print(f"\nMelhor correspondência: {melhor_valor} com score {melhor_score:.4f}")

    if melhor_score < 0.85:
        print("AVISO: Similaridade baixa. Resultado pode não ser confiável.")

    return melhor_valor

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python main3.py caminho_da_imagem")
        sys.exit(1)

    caminho_imagem_teste = sys.argv[1]

    if not os.path.exists(caminho_imagem_teste):
        print(f"Caminho inválido: {caminho_imagem_teste}")
        sys.exit(1)

    reconhecido = reconhecer_numero(caminho_imagem_teste, tamanho=TAMANHO_DESEJADO)
    print(f"\nNúmero reconhecido: {reconhecido}")
