import React, { createContext, useState, useEffect, useContext } from "react";

import { initializeApp } from "firebase/app";
import {
    getAuth,
    GoogleAuthProvider,
    signInWithPopup,
    signOut,
    onAuthStateChanged,
} from "firebase/auth";
import { useAPI } from "./APIContext";

const firebaseConfig = {
    apiKey: import.meta.env.VITE_API_KEY,
    authDomain: import.meta.env.VITE_AUTH_DOMAIN,
    projectId: import.meta.env.VITE_PROJECT_ID,
    storageBucket: import.meta.env.VITE_STORAGE_BUCKET,
    messagingSenderId: import.meta.env.VITE_MESSAGING_SENDER_ID,
    appId: import.meta.env.VITE_APP_ID,
    measurementId: import.meta.env.VITE_MEASUREMENT_ID,
};

const app = initializeApp(firebaseConfig);
const auth = getAuth(app);

const AuthContext = createContext();

export const AuthProvider = ({ children }) => {
    const { authAPI, users } = useAPI();

    const [user, setUser] = useState(undefined);
    const [loading, setLoading] = useState(true);

    // Función para recuperar el token almacenado
    const obtenerToken = () => {
        return localStorage.getItem("oauth_token");
    };

    const getUser = () => user;
    const reloadUserFromDatabase = async () => {
        const userResponse = await users.getById(user.uid);
        if (userResponse.status >= 200 && userResponse.status < 300) {
            setUser(userResponse.data);
        }
    }

    const handleAuth = async (user) => {
        try {
            const userResponse = await users.getById(user.uid);
            if (userResponse.status >= 200 && userResponse.status < 300) {
                const accessToken = await user.getIdToken(true); // Para que se renueve cuando entras
                await handleLogin(accessToken);
            } else await handleRegister(user.accessToken);
        } catch (error) {
            console.error("Auth error:", error);
        } finally {
            setLoading(false);
        }
    };

    const handleLogin = async (accessToken, show = true) => {
        try {
            const loginResponse = await authAPI.login({ token: accessToken });
            if (loginResponse.status >= 200 && loginResponse.status < 300) {
                setUser(loginResponse.data);
                localStorage.setItem("oauth_token", accessToken);
            } else {
                await logout();
            }
        } catch (error) {
            console.error("Login error:", error);
        } finally {
            setLoading(false);
        }
    };

    const handleRegister = async (accessToken) => {
        try {
            const registerResponse = await authAPI.register({ token: accessToken });
            if (registerResponse.status >= 200 && registerResponse.status < 300) {
                setUser(registerResponse.data.result);
                localStorage.setItem("oauth_token", accessToken);
            } else {
                await logout();
            }
        } catch (error) {
            console.error("Register error:", error);
        }
    };

    const handleLogout = async () => {
        try {
            const logoutResponse = await authAPI.logout();
            if (logoutResponse.status >= 200 && logoutResponse.status < 300) {
                setUser(undefined);
                localStorage.removeItem("oauth_token");
            } else {
                console.error("Logout failed:", logoutResponse);
            }
        } catch (error) {
            console.error("Logout error:", error);
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        const subscribe = onAuthStateChanged(auth, (user) => {
            setLoading(true);
            if (user) handleAuth(user);
            else {
                const token = obtenerToken();
                if (token) {
                    setUser({ token });
                } else {
                    setLoading(false);
                }
            }
        });

        return () => subscribe();
    }, []);

    useEffect(() => {
        const renewTokenInterval = setInterval(async () => {
            const currentUser = auth.currentUser;
            if (currentUser) {
                try {
                    const token = await currentUser.getIdToken(true);
                    await handleLogin(token, false);
                } catch (error) {
                    await logout();
                    console.error("Error al renovar el token:", error);
                }
            }
        }, 30 * 60 * 1000); // Cada 30 minutos se renueva el token

        return () => clearInterval(renewTokenInterval);
    }, []);

    const login = async () => {
        const provider = new GoogleAuthProvider();
        try {
            const result = await signInWithPopup(auth, provider);
            const user = result.user;

            return user;
        } catch (error) {
            console.error(error);
        }
    };

    const logout = async () => {
        try {
            await handleLogout();
            await signOut(auth);
        } catch (error) {
            console.error(error);
        }
    };

    const isLogged = () => {
        return user !== undefined;
    };

    return (
        <AuthContext.Provider
            value={{
                getUser,
                reloadUserFromDatabase,
                login,
                logout,
                isLogged,
                obtenerToken,
            }}
        >
            {loading ? <div className="d-flex justify-content-center align-items-center vh-100">
                <div className="spinner-border text-warning me-3" style={{fontSize: "20px", scale: "2"}}></div>
            </div> : children}
        </AuthContext.Provider>
    );
};

export const useAuth = () => useContext(AuthContext);