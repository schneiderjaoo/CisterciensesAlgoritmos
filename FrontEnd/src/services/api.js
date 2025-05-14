export const API_URL = "http://127.0.0.1:5000";

export const gerarNumero = async (numero) => {
  const response = await fetch(`${API_URL}/gerar/${numero}`);
  return response.json();
};

export const reconhecerNumero = async (file) => {
  const formData = new FormData();
  formData.append("imagem", file);

  const response = await fetch(`${API_URL}/reconhecer`, {
    method: "POST",
    body: formData,
  });
  return response.json();
};

export const obterImagem = (nomeImagem) => {
  return `${API_URL}/imagem/${nomeImagem}`;
};
