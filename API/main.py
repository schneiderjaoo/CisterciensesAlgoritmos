from flask import Flask, send_from_directory, jsonify, request
from flask_cors import CORS
import os
import uuid
from services.cisterciense_service import gerar_numero_cisterciense
from services.reconhecimento_service import reconhecer_numero 

app = Flask(__name__)
CORS(app)

DIRETORIO_OUTPUT = os.path.join(os.getcwd(), "static", "output")
UPLOAD_TEMP = os.path.join(os.getcwd(), "static", "temp")
os.makedirs(UPLOAD_TEMP, exist_ok=True)

@app.route("/gerar/<int:numero>")
def gerar(numero):
    try:
        caminho_imagem, imagens_aux = gerar_numero_cisterciense(numero)
        return jsonify({
            "imagem_principal": "numero_gerado.png",
            "imagens_auxiliares": imagens_aux
        })
    except Exception as e:
        print(f"Erro na API: {str(e)}")  
        return jsonify({"erro": str(e)}), 500

@app.route("/imagem/<nome>")
def obter_imagem(nome):
    return send_from_directory(DIRETORIO_OUTPUT, nome)

@app.route("/reconhecer", methods=["POST"])
def reconhecer():
    if "imagem" not in request.files:
        return jsonify({"erro": "Arquivo de imagem não encontrado"}), 400

    imagem = request.files["imagem"]
    if imagem.filename == "":
        return jsonify({"erro": "Nenhum arquivo selecionado"}), 400

    try:
        print(f"Recebida imagem: {imagem.filename}")
        nome_arquivo = f"{uuid.uuid4().hex}.png"
        caminho_temporario = os.path.join(UPLOAD_TEMP, nome_arquivo)
        imagem.save(caminho_temporario)
        print(f"Imagem salva temporariamente em: {caminho_temporario}")

        numero_reconhecido = reconhecer_numero(caminho_temporario, tamanho=(93, 133))
        print(f"Número reconhecido: {numero_reconhecido}")

        os.remove(caminho_temporario)
        return jsonify({"numero_reconhecido": numero_reconhecido})

    except Exception as e:
        print(f"Erro no reconhecimento: {str(e)}")
        return jsonify({"erro": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True)
