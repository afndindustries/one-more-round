import React from 'react';
import 'bootstrap/dist/css/bootstrap.min.css';
import "./LoginPage.css";
import GoogleLogo from "../../assets/google.svg";
import { Link } from 'react-router-dom';

const LoginPage = () => {
    return (
        <main className="container-fluid d-flex justify-content-center align-items-center login-bg">
            <div class="particles">
                <span style={{top: "10%", left: "20%", animationDelay: "0s"}}></span>
                <span style={{top: "50%", left: "70%", animationDelay: "2s"}}></span>
                <span style={{top: "30%", left: "40%", animationDelay: "4s"}}></span>
                <span style={{top: "80%", left: "10%", animationDelay: "1s"}}></span>
                <span style={{top: "60%", left: "90%", animationDelay: "3s"}}></span>
            </div>
            <div className="card p-4 shadow-sm" style={{ width: '100%', maxWidth: '400px' }}>
                <div className="text-center mb-4">
                    <h2 className="h3 font-weight-normal">Iniciar Sesión</h2>
                    <button className="google-btn">
                        <img
                            src={GoogleLogo}
                            alt="Google Logo"
                            className="google-logo"
                            style={{ color: 'red' }}
                        />
                        Iniciar sesión con Google
                    </button>
                    <Link to={"/"} className='btn btn-link mt-3' style={{textDecoration: 'none'}}>
                        Volver
                    </Link>
                </div>
            </div>
        </main>
    );
};

export default LoginPage;