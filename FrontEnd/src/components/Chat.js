import React, { useState } from "react";
import "../App.css";
import Message from "./Message";
import ImageMessage from "./ImageMessage";
import InputSection from "./InputSection";
import LoadingIndicator from "./LoadingIndicator";
import { gerarNumero, reconhecerNumero, obterImagem } from "../services/api";

const Chat = () => {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");
  const [imageUrl, setImageUrl] = useState(null);
  const [auxImages, setAuxImages] = useState([]);
  const [numeroSolicitado, setNumeroSolicitado] = useState(null);
  const [isLoading, setIsLoading] = useState(false);

  const adicionarMensagem = (msg) => {
    setMessages((prev) => [...prev, msg]);
  };

  const limparChat = () => {
    setMessages([]);
    setImageUrl(null);
    setAuxImages([]);
    setNumeroSolicitado(null);
  };

  const handleSendMessage = async () => {
    const numero = parseInt(input.trim(), 10);

    if (isNaN(numero)) {
      setMessages([{ sender: "Sistema", text: "Por favor, digite um número válido." }]);
      return;
    }

    setNumeroSolicitado(numero);
    setMessages([{ sender: "Usuário", text: input }]);
    setInput("");
    setIsLoading(true);

    try {
      const data = await gerarNumero(numero);

      if (data?.imagem_principal) {
        setImageUrl(`${obterImagem(data.imagem_principal)}?t=${Date.now()}`);
        setAuxImages(data.imagens_auxiliares.map(obterImagem));

        setMessages([
          { sender: "Usuário", text: input },
          { sender: "Sistema", text: "" },
        ]);
      } else {
        setMessages([
          { sender: "Usuário", text: input },
          { sender: "Sistema", text: "Erro ao gerar a imagem." },
        ]);
      }
    } catch {
      setMessages([
        { sender: "Usuário", text: input },
        { sender: "Sistema", text: "Falha ao conectar com a API." },
      ]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleImageUpload = async (e) => {
    const file = e.target.files?.[0];
    if (!file) return;

    limparChat();

    const reader = new FileReader();
    reader.onload = () => {
      adicionarMensagem({
        sender: "Usuário",
        text: "Imagem enviada:",
        image: reader.result,
      });
    };
    reader.readAsDataURL(file);

    setIsLoading(true);

    try {
      const data = await reconhecerNumero(file);

      if (data?.numero_reconhecido !== undefined) {
        adicionarMensagem({
          sender: "Sistema",
          text: `Esse símbolo é referente ao número ${data.numero_reconhecido}`,
        });
      } else {
        adicionarMensagem({
          sender: "Sistema",
          text: "Não foi possível reconhecer o número.",
        });
      }
    } catch (error) {
      console.error("Erro ao enviar imagem:", error);
      adicionarMensagem({
        sender: "Sistema",
        text: "Erro ao processar a imagem.",
      });
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div id="chat-container">
      <div id="chat-header">Chat dos Números Cistercienses 🔢</div>

      <div id="chat-box">
        {messages.map((msg, index) => (
          <Message key={index} sender={msg.sender} text={msg.text} image={msg.image} />
        ))}

        {messages.some((msg) => msg.sender === "Sistema") && imageUrl && (
          <ImageMessage
            imageUrl={imageUrl}
            auxImages={auxImages}
            numeroSolicitado={numeroSolicitado}
          />
        )}
      </div>

      {isLoading && <LoadingIndicator />}

      <InputSection
        input={input}
        setInput={setInput}
        onSendMessage={handleSendMessage}
        onImageUpload={handleImageUpload}
      />
    </div>
  );
};

export default Chat;
