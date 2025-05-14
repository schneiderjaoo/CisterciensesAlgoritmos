import React from "react";
import Chat from "./components/Chat";
import logo from "./assets/catolica.png";
import "./App.css";

function App() {
  return (
    <div className="App">
      <Chat />
      <img src={logo} alt="Católica SC" className="logo" />
    </div>
  );
}

export default App;
