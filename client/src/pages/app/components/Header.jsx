import React, { useState } from "react";
import { useNavigate } from "react-router-dom";

const Header = () => {
    const navigate = useNavigate();

    return (
        <nav className="navbar navbar-expand-lg navbar-light bg-white shadow-sm border-bottom">
          <div className="container">
            <span
              className="navbar-brand text-dark display-4 mb-0 pb-0"
              onClick={() => navigate("/")}
              style={{ fontWeight: 'bold', cursor: "pointer" }}
            >
              OneMoreRound
            </span>
    
            <button
              className="navbar-toggler"
              type="button"
              data-bs-toggle="collapse"
              data-bs-target="#navbarNav"
              aria-controls="navbarNav"
              aria-expanded="false"
              aria-label="Toggle navigation"
            >
              <span className="navbar-toggler-icon"></span>
            </button>
    
            <div className="collapse navbar-collapse" id="navbarNav">
              <div className="ms-auto"></div>
    
              <button
                className="btn btn-primary"
                onClick={() => navigate("/login")}
              >
                Iniciar sesión
              </button>
            </div>
          </div>
        </nav>
      );
};

export default Header;
