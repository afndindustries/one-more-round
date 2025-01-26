import React from "react";
import { useNavigate } from "react-router-dom";

const NotFoundPage = () => {
    const navigate = useNavigate();

    return (
        <div
            className="container-fluid d-flex justify-content-center align-items-center vh-100">
            <div className="text-center">
                <div className="display-1 text-danger" style={{ fontWeight: 'bold' }}>404</div>
                <p className="lead text-muted">¡Ups! La página que buscas no se encuentra.</p>
                <p className="text-secondary mb-4">Parece que la página ha desaparecido o nunca existió. Pero no te preocupes, siempre hay una solución.</p>
                <span style={{ cursor: "pointer" }} onClick={() => navigate("/")} className="btn btn-lg btn-primary shadow-lg">Volver al inicio</span>
            </div>
        </div>
    );
}

export default NotFoundPage;
