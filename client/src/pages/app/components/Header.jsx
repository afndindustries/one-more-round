import React, { useState } from "react";
import { useNavigate } from "react-router-dom";

const Header = () => {
    const navigate = useNavigate();

    return (
        <nav className="navbar navbar-expand-lg navbar-light bg-white shadow-sm border-bottom">
            <div className="container">
                <span className="navbar-brand text-dark display-4 mb-0 pb-0"
                    onClick={() => navigate("/")} style={{ fontWeight: 'bold', cursor: "pointer" }}>
                    OneMoreRound
                </span>
            </div>
        </nav>
    );
};

export default Header;
