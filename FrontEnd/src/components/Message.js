import React from "react";
import "../App.css";

const Message = ({ sender, text, image }) => {
  return (
    <div className={`message-container ${sender}`}>
      <div className="message-content">
        <i className={sender === "Usuário" ? "fas fa-user" : "fas fa-robot"}></i>
        <b>{sender}:</b> {text}
        {image && (
          <div className="image-container">
            <img src={image} alt="Imagem enviada" className="numero-imagem" />
          </div>
        )}
      </div>
    </div>
  );
};

export default Message;
