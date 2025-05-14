import os
import cv2
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
from joblib import dump

# Caminho para as imagens rotuladas
DIRETORIO_DATASET = os.path.join("static", "symbols", "dataset")

def extrair_hu_moments(path_imagem):
    img = cv2.imread(path_imagem, cv2.IMREAD_GRAYSCALE)  
    if img is None:
        print(f"[AVISO] Imagem inválida ou não carregada: {path_imagem}")
        return None

    # Redimensiona para padrão
    img = cv2.resize(img, (128, 128))

    # Inverte a imagem para garantir que o símbolo esteja em branco sobre fundo preto
    img = cv2.bitwise_not(img)

    # Binariza
    _, binarizada = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY)

    # Encontra os contornos
    contornos, _ = cv2.findContours(binarizada, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if not contornos:
        print(f"[AVISO] Nenhum contorno encontrado em: {path_imagem}")
        return None

    # Pega o maior contorno
    maior = max(contornos, key=cv2.contourArea)

    # Calcula os Hu Moments
    hu = cv2.HuMoments(cv2.moments(maior)).flatten()
    return -np.sign(hu) * np.log10(np.abs(hu) + 1e-10)

# Dataset
X = []
y = []

# Carregar imagens
for nome_arquivo in os.listdir(DIRETORIO_DATASET):
    if nome_arquivo.endswith(".png"):
        try:
            rotulo = int(nome_arquivo.split(".")[0])
        except ValueError:
            print(f"[ERRO] Nome de arquivo inválido para rotulagem: {nome_arquivo}")
            continue

        caminho = os.path.join(DIRETORIO_DATASET, nome_arquivo)
        hu = extrair_hu_moments(caminho)
        if hu is not None:
            X.append(hu)
            y.append(rotulo)

print(f"[INFO] Total de imagens válidas: {len(X)}")

# Validar quantidade de dados
if len(X) < 2:
    raise ValueError("Poucas imagens válidas para treinar o modelo. Adicione mais imagens ao diretório.")

# Converter para array
X = np.array(X)
y = np.array(y)

# Treinar modelo
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
modelo = RandomForestClassifier(n_estimators=100, random_state=42)
modelo.fit(X_train, y_train)

# Avaliação
y_pred = modelo.predict(X_test)
print(classification_report(y_test, y_pred))

# Salvar modelo
dump(modelo, "modelo_cisterciense.joblib")
print("Modelo salvo como modelo_cisterciense.joblib")
