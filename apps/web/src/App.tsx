import { BrowserRouter, Routes, Route, NavLink, Link } from "react-router-dom";
import { AuthProvider, useAuth } from "./context/AuthContext";
import { ProtectedRoute } from "./components/ProtectedRoute";

import CitizenPage from "./pages/CitizenPage";
import DashboardPage from "./pages/DashboardPage";
import ReviewerPage from "./pages/ReviewerPage";
import LoginPage from "./pages/LoginPage";

function NavigationHeader() {
  const { user, isAuthenticated, logout } = useAuth();

  return (
    <header className="sticky top-0 z-50 border-b border-slate-200/80 bg-white/80 backdrop-blur-md transition-all">
      <div className="mx-auto flex max-w-7xl items-center justify-between px-4 py-3.5 sm:px-6 lg:px-8">
        <Link
          to="/"
          className="group flex items-center gap-3 transition-transform active:scale-95"
        >
          <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-gradient-to-tr from-blue-600 via-indigo-600 to-violet-600 font-extrabold text-white shadow-md shadow-blue-500/20 group-hover:shadow-blue-500/35 transition-all">
            S
          </div>
          <div className="flex flex-col">
            <span className="text-lg font-bold tracking-tight text-slate-900 group-hover:text-blue-600 transition-colors">
              SANKALP
            </span>
            <span className="text-[11px] font-medium text-slate-500 tracking-wide uppercase">
              Citizen Intelligence Platform
            </span>
          </div>
        </Link>

        <nav className="flex items-center gap-1.5 rounded-full bg-slate-100/80 p-1 border border-slate-200/60 shadow-inner">
          <NavLink
            to="/"
            end
            className={({ isActive }) =>
              `rounded-full px-4 py-1.5 text-xs font-semibold transition-all duration-200 ${
                isActive
                  ? "bg-white text-blue-600 shadow-sm shadow-slate-200"
                  : "text-slate-600 hover:text-slate-900 hover:bg-slate-200/50"
              }`
            }
          >
            Citizen Voice
          </NavLink>

          <NavLink
            to="/dashboard"
            className={({ isActive }) =>
              `rounded-full px-4 py-1.5 text-xs font-semibold transition-all duration-200 ${
                isActive
                  ? "bg-white text-blue-600 shadow-sm shadow-slate-200"
                  : "text-slate-600 hover:text-slate-900 hover:bg-slate-200/50"
              }`
            }
          >
            Intelligence Dashboard
          </NavLink>

          <NavLink
            to="/reviewer"
            className={({ isActive }) =>
              `rounded-full px-4 py-1.5 text-xs font-semibold transition-all duration-200 ${
                isActive
                  ? "bg-white text-blue-600 shadow-sm shadow-slate-200"
                  : "text-slate-600 hover:text-slate-900 hover:bg-slate-200/50"
              }`
            }
          >
            Reviewer Portal
          </NavLink>
        </nav>

        {/* User Auth Info & Logout Button */}
        <div className="flex items-center gap-3">
          {isAuthenticated && user ? (
            <div className="flex items-center gap-3">
              <div className="hidden sm:flex flex-col text-right">
                <span className="text-xs font-bold text-slate-800">{user.full_name}</span>
                <span className="text-[10px] font-semibold text-blue-600 uppercase tracking-wider">
                  {user.role}
                </span>
              </div>
              <button
                onClick={logout}
                className="rounded-full border border-slate-200 bg-slate-50 px-3 py-1.5 text-xs font-semibold text-slate-600 hover:bg-red-50 hover:text-red-600 hover:border-red-200 transition-all cursor-pointer"
              >
                Sign Out
              </button>
            </div>
          ) : (
            <Link
              to="/login"
              className="rounded-full bg-slate-900 px-4 py-1.5 text-xs font-semibold text-white shadow-sm hover:bg-slate-800 transition-all"
            >
              Sign In
            </Link>
          )}
        </div>
      </div>
    </header>
  );
}

export default function App() {
  return (
    <BrowserRouter>
      <AuthProvider>
        <div className="min-h-screen bg-slate-50/60 font-sans text-slate-800 antialiased">
          <NavigationHeader />

          {/* Main Routes */}
          <Routes>
            <Route path="/" element={<CitizenPage />} />
            <Route path="/dashboard" element={<DashboardPage />} />
            <Route path="/login" element={<LoginPage />} />
            <Route
              path="/reviewer"
              element={
                <ProtectedRoute allowedRoles={["admin", "reviewer"]}>
                  <ReviewerPage />
                </ProtectedRoute>
              }
            />
          </Routes>
        </div>
      </AuthProvider>
    </BrowserRouter>
  );
}