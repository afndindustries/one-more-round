import { createRoot } from 'react-dom/client';
import { APIProvider } from './context/APIContext.jsx';
import { AuthProvider } from './context/AuthContext.jsx';

import App from "./pages/app/App.jsx";

import "bootstrap/dist/css/bootstrap.min.css";
import "bootstrap/dist/js/bootstrap.bundle.js";
import "bootstrap-icons/font/bootstrap-icons.css";
import "./index.css"

createRoot(document.getElementById('root')).render(
    <APIProvider>
        <AuthProvider>
            <App />
        </AuthProvider>
    </APIProvider>
)
