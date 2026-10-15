import { createContext, useContext, useEffect, useState } from "react";
import { getCurrentUser } from "../api/auth";

const AuthContext = createContext(null);

export function AuthProvider({ children }) {
    const [user, setUser] = useState(null);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        let active = true;

        async function loadUser() {
            const token = localStorage.getItem("access_token");

            if (!token) {
                setUser(null);
                setLoading(false);
                return;
            }

            try {
                const currentUser = await getCurrentUser();

                if (active) {
                    setUser(currentUser);
                }
            } catch (error) {
                if (active) {
                    setUser(null);
                }
            } finally {
                if (active) {
                    setLoading(false);
                }
            }
        }

        loadUser();

        return () => {
            active = false;
        };
    }, []);

    function logout() {
        localStorage.removeItem("access_token");
        setUser(null);
    }

    const value = {
        user,
        loading,
        setUser,
        logout,
    };

    return (
        <AuthContext.Provider value={value}>
            {children}
        </AuthContext.Provider>
    );
}

export function useAuth() {
    const context = useContext(AuthContext);

    if (context === null) {
        throw new Error("useAuth must be used within an AuthProvider");
    }

    return context;
}