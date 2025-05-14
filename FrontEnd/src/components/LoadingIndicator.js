import React from "react";
import "../App.css";

const LoadingIndicator = () => {
  return (
    <div className="loading-indicator">
      <i className="fas fa-spinner fa-spin"></i> Verificando imagem...
    </div>
  );
};

export default LoadingIndicator;
