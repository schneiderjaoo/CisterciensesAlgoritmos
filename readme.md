Conversor de Algarismos Cistercienses com Visão Computacional
Este projeto combina história medieval com tecnologia moderna, oferecendo uma aplicação interativa capaz de converter números entre o sistema arábico (1–9999) e o sistema cisterciense, utilizado por monges entre os séculos XII e XV.

Utilizando visão computacional (OpenCV) e uma interface intuitiva (React + Flask), o sistema permite:

Gerar e exibir numerais cistercienses a partir de números arábicos.

Reconhecer numerais cistercienses em imagens e convertê-los para números arábicos.

Interagir com a aplicação por meio de um chat visual e dinâmico.

🕰️ Um Pouco de História
Entre os séculos XII e XV, monges da Ordem de Cister desenvolveram um sistema numérico único e engenhoso. Combinando traços em torno de uma linha vertical, os algarismos cistercienses conseguiam representar números de 1 a 9999 com um único símbolo.

Embora não utilizados em cálculos, esses numerais serviram como uma alternativa compacta aos números romanos, sendo empregados em manuscritos, inventários e marcações de produção.

⚙️ Funcionalidades Principais
🔁 Conversão Bidirecional
➡️ Arábico → Cisterciense
Entrada: Número entre 1 e 9999
Saída: Imagem gerada com o símbolo cisterciense correspondente

⬅️ Cisterciense → Arábico
Entrada: Imagem contendo um símbolo cisterciense
Saída: Número arábico interpretado via modelo de reconhecimento

🖼️ Processamento de Imagens
Geração de imagens precisas e livres de distorções

Leitura automatizada de símbolos a partir de imagens locais

Visualização em frontend com:

Imagem original

Número detectado

Localização gráfica dos elementos

🧰 Tecnologias
Python 3.12

OpenCV – Manipulação e reconhecimento de imagem

Flask – Backend RESTful

React – Interface moderna e interativa

JavaScript / HTML / CSS

📁 Estrutura do Projeto
bash
Copiar
Editar
├── API/                       # Backend Flask
│   ├── SERVICES/              # Lógicas de conversão e reconhecimento
│   ├── static/                # Imagens geradas, símbolos e temporários
│   ├── main.py                # Ponto de entrada Flask
│   ├── treinar_modelo.py      # Treinamento do modelo de reconhecimento
│   └── requirements.txt       # Dependências Python
├── FrontEnd/                  # Aplicação React
│   ├── public/                # HTML principal
│   ├── src/                   # Código React e componentes
│   │   ├── components/        # Interface modular
│   │   ├── services/          # Comunicação com a API
│   │   ├── assets/            # Imagens e ícones
│   │   ├── App.js             # Componente principal
│   │   └── index.js           # Bootstrap do React
└── README.md
🚀 Como Rodar o Projeto
Você precisará de dois terminais para executar backend e frontend separadamente.

Pré-requisitos
Python 3.12+

Node.js 18.12+ e npm

1️⃣ Clonar o Repositório
bash
Copiar
Editar
git clone https://github.com/seu-usuario/seu-repositorio.git
cd seu-repositorio
2️⃣ Executar o Backend (Flask)
bash
Copiar
Editar
cd API

# Criar ambiente virtual
python -m venv venv

# Ativar ambiente
# Linux/macOS
source venv/bin/activate
# Windows
venv\Scripts\activate

# Instalar dependências
pip install -r requirements.txt

# Rodar servidor
python main.py
A API será acessível em http://localhost:5000

3️⃣ Executar o Frontend (React)
bash
Copiar
Editar
cd FrontEnd

# Instalar dependências
npm install

# Iniciar frontend
npm start
A interface será aberta em http://localhost:3000

💬 Como Usar
A aplicação funciona via uma interface de chat interativo:

Para gerar um número cisterciense, basta digitar um valor entre 1 e 9999.

Para interpretar uma imagem, clique no ícone de clipe e envie uma imagem com o símbolo cisterciense.

Exemplos:
🔢 Entrada de número:


🖼️ Entrada de imagem:


📌 Considerações Finais
Este projeto é uma demonstração prática da integração entre inteligência computacional, design de interfaces modernas e valores históricos. É ideal para fins educacionais, experimentações com visão computacional e valorização da história da matemática.