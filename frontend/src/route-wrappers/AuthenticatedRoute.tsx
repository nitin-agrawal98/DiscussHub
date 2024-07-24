import { Navigate, Outlet, useLocation } from "react-router-dom";
import { useContext } from "react";
import { AuthContext } from "../auth/AuthContextProvider";

const AuthenticatedRoute: React.FC = () => {
    const authContext = useContext(AuthContext);
    const location = useLocation();

    if (authContext?.token === '') {
        return (
            <Navigate
                to="/signin"
                state={{redirect: `${location.pathname}${location.search}`}}
            />
        );
    }
    return <Outlet />;
};

export default AuthenticatedRoute;