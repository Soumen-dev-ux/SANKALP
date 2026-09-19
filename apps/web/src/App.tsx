import { BrowserRouter, Routes, Route, NavLink, Link } from "react-router-dom";

import CitizenPage from "./pages/CitizenPage";
import DashboardPage from "./pages/DashboardPage";

export default function App() {
  return (
    <BrowserRouter>
      <div className="min-h-screen bg-slate-50/60 font-sans text-slate-800 antialiased">
        {/* Sticky Glassmorphic Header */}
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
            </nav>
          </div>
        </header>

        {/* Main Routes */}
        <Routes>
          <Route path="/" element={<CitizenPage />} />
          <Route path="/dashboard" element={<DashboardPage />} />
        </Routes>
      </div>
    </BrowserRouter>
  );
}