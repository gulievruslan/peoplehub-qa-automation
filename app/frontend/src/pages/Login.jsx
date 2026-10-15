import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { getCurrentUser, login } from "../api/auth";
import { useAuth } from "../context/AuthContext";
import "../App.css";

function Login() {
    const navigate = useNavigate();
    const { setUser } = useAuth();

    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");
    const [error, setError] = useState("");
    const [loading, setLoading] = useState(false);

    async function handleSubmit(event) {
        event.preventDefault();
        setError("");

        if (!email.trim() || !password) {
            setError("Email and password are required.");
            return;
        }

        setLoading(true);

        try {
            const data = await login(email.trim(), password);

            localStorage.setItem("access_token", data.access_token);

            try {
                const currentUser = await getCurrentUser();

                setUser(currentUser);
                navigate("/dashboard", { replace: true });
            } catch (userError) {
                localStorage.removeItem("access_token");
                setUser(null);
                throw userError;
            }
        } catch (loginError) {
            const message =
                typeof loginError?.message === "string"
                    ? loginError.message
                    : "Unable to sign in. Please check your credentials and try again.";

            setError(message);
        } finally {
            setLoading(false);
        }
    }

    return (
        <div className="login-page">
            <div className="login-card">
                <h1>PeopleHub</h1>

                <p className="login-subtitle">
                    Employee Management Platform
                </p>

                <form onSubmit={handleSubmit}>
                    <label htmlFor="email">Email</label>

                    <input
                        id="email"
                        type="email"
                        placeholder="Enter your email"
                        value={email}
                        onChange={(event) => setEmail(event.target.value)}
                        autoComplete="username"
                    />

                    <label htmlFor="password">Password</label>

                    <input
                        id="password"
                        type="password"
                        placeholder="Enter your password"
                        value={password}
                        onChange={(event) => setPassword(event.target.value)}
                        autoComplete="current-password"
                    />

                    {error && (
                        <p className="login-error" role="alert">
                            {error}
                        </p>
                    )}

                    <button type="submit" disabled={loading}>
                        {loading ? "Signing in..." : "Sign in"}
                    </button>
                </form>
            </div>
        </div>
    );
}

export default Login;