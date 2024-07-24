import React, { useContext } from "react";
import { Navigate, Outlet, useLocation } from "react-router-dom";
import { AuthContext } from "../auth/AuthContextProvider";

const UnauthenticatedRoute: React.FC = () => {
    const authContext = useContext(AuthContext);
    const location = useLocation();

    if (authContext?.token) {
        const next = location.state ? location.state['redirect'] : '/';
        return <Navigate to={next} />;
    }
    return <Outlet />;
}

export default UnauthenticatedRoute;