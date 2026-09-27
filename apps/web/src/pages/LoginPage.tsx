import React, { useState } from "react";
import { useNavigate, useLocation } from "react-router-dom";
import { useAuth } from "../context/AuthContext";

export default function LoginPage() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState<string | null>(null);
  const [isSubmitting, setIsSubmitting] = useState(false);

  const { login } = useAuth();
  const navigate = useNavigate();
  const location = useLocation();

  const from = (location.state as { from?: { pathname: string } })?.from?.pathname || "/reviewer";

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);
    setIsSubmitting(true);

    try {
      await login({ email, password });
      navigate(from, { replace: true });
    } catch (err: any) {
      console.error("Login failed:", err);
      const msg = err.response?.data?.error?.message || err.response?.data?.detail || "Invalid email or password";
      setError(msg);
    } finally {
      setIsSubmitting(false);
    }
  };

  const handleQuickLogin = (quickEmail: string) => {
    setEmail(quickEmail);
    setPassword("password123");
  };

  return (
    <div className="flex min-h-[calc(100vh-80px)] items-center justify-center px-4 py-12">
      <div className="w-full max-w-md space-y-6">
        {/* Header Branding */}
        <div className="text-center">
          <div className="mx-auto flex h-14 w-14 items-center justify-center rounded-2xl bg-gradient-to-tr from-blue-600 via-indigo-600 to-violet-600 text-2xl font-extrabold text-white shadow-lg shadow-blue-500/25">
            S
          </div>
          <h1 className="mt-4 text-2xl font-bold tracking-tight text-slate-900">
            Sign In to SANKALP
          </h1>
          <p className="mt-1 text-xs font-medium text-slate-500">
            Authenticated Portal for Human Reviewers & Operations
          </p>
        </div>

        {/* Form Card */}
        <div className="rounded-3xl border border-slate-200/80 bg-white p-8 shadow-xl shadow-slate-200/50 backdrop-blur-xl">
          {error && (
            <div className="mb-6 rounded-xl border border-red-200 bg-red-50/80 p-3.5 text-xs text-red-700">
              <span className="font-semibold">Authentication Error:</span> {error}
            </div>
          )}

          <form onSubmit={handleSubmit} className="space-y-4">
            <div>
              <label className="block text-xs font-semibold uppercase tracking-wider text-slate-600">
                Email Address
              </label>
              <input
                type="email"
                required
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                placeholder="reviewer@sankalp.gov"
                className="mt-1.5 w-full rounded-xl border border-slate-200 bg-slate-50/50 px-4 py-2.5 text-sm text-slate-800 placeholder:text-slate-400 focus:border-blue-500 focus:bg-white focus:outline-none focus:ring-2 focus:ring-blue-500/20 transition-all"
              />
            </div>

            <div>
              <label className="block text-xs font-semibold uppercase tracking-wider text-slate-600">
                Password
              </label>
              <input
                type="password"
                required
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                placeholder="••••••••"
                className="mt-1.5 w-full rounded-xl border border-slate-200 bg-slate-50/50 px-4 py-2.5 text-sm text-slate-800 placeholder:text-slate-400 focus:border-blue-500 focus:bg-white focus:outline-none focus:ring-2 focus:ring-blue-500/20 transition-all"
              />
            </div>

            <button
              type="submit"
              disabled={isSubmitting}
              className="mt-2 w-full rounded-xl bg-gradient-to-r from-blue-600 to-indigo-600 py-3 text-sm font-semibold text-white shadow-md shadow-blue-500/25 hover:from-blue-700 hover:to-indigo-700 focus:outline-none focus:ring-2 focus:ring-blue-500/40 disabled:opacity-50 transition-all cursor-pointer"
            >
              {isSubmitting ? "Authenticating..." : "Sign In"}
            </button>
          </form>

          {/* Quick Login Presets */}
          <div className="mt-8 border-t border-slate-100 pt-6">
            <p className="text-center text-[11px] font-semibold uppercase tracking-wider text-slate-400">
              Quick Test Credentials
            </p>
            <div className="mt-3 grid grid-cols-2 gap-2">
              <button
                type="button"
                onClick={() => handleQuickLogin("admin@sankalp.gov")}
                className="rounded-lg border border-slate-200 bg-slate-50 px-3 py-2 text-left text-xs hover:border-blue-300 hover:bg-blue-50/50 transition-colors cursor-pointer"
              >
                <div className="font-semibold text-slate-700">Admin Account</div>
                <div className="text-[10px] text-slate-400">admin@sankalp.gov</div>
              </button>
              <button
                type="button"
                onClick={() => handleQuickLogin("reviewer@sankalp.gov")}
                className="rounded-lg border border-slate-200 bg-slate-50 px-3 py-2 text-left text-xs hover:border-blue-300 hover:bg-blue-50/50 transition-colors cursor-pointer"
              >
                <div className="font-semibold text-slate-700">Reviewer Account</div>
                <div className="text-[10px] text-slate-400">reviewer@sankalp.gov</div>
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
