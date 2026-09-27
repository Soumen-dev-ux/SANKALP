import React from "react";
import { Navigate, useLocation } from "react-router-dom";
import { useAuth } from "../context/AuthContext";

interface ProtectedRouteProps {
  children: React.ReactElement;
  allowedRoles?: string[];
}

export const ProtectedRoute: React.FC<ProtectedRouteProps> = ({
  children,
  allowedRoles = ["admin", "reviewer"],
}) => {
  const { user, isLoading, isAuthenticated } = useAuth();
  const location = useLocation();

  if (isLoading) {
    return (
      <div className="flex h-96 items-center justify-center">
        <div className="flex flex-col items-center gap-3">
          <div className="h-10 w-10 animate-spin rounded-full border-4 border-blue-600 border-t-transparent"></div>
          <p className="text-xs font-semibold text-slate-500">Verifying session credentials...</p>
        </div>
      </div>
    );
  }

  if (!isAuthenticated || !user) {
    return <Navigate to="/login" state={{ from: location }} replace />;
  }

  if (allowedRoles.length > 0 && !allowedRoles.includes(user.role)) {
    return (
      <div className="mx-auto max-w-2xl px-4 py-16 text-center">
        <div className="rounded-2xl border border-red-200 bg-red-50/70 p-8 text-red-800 shadow-sm">
          <h2 className="text-xl font-bold">Access Restricted</h2>
          <p className="mt-2 text-sm text-red-600">
            Your current role (<span className="font-semibold uppercase">{user.role}</span>) does not have authorization to view this reviewer workspace.
          </p>
        </div>
      </div>
    );
  }

  return children;
};
