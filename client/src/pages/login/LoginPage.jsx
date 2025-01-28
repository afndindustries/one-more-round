import React from 'react';
import 'bootstrap/dist/css/bootstrap.min.css';
import "./LoginPage.css";
import GoogleLogo from "../../assets/google.svg";
import { Link } from 'react-router-dom';

const LoginPage = () => {
    return (
        <div className="container-fluid vh-100 d-flex justify-content-center align-items-center login-bg">
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
        </div>
    );
};

export default LoginPage;