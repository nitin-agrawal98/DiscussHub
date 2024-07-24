import { useContext } from "react";
import { TOKEN } from "../constants/localstorage";
import { AuthContext } from "../auth/AuthContextProvider";

const useLogout = () => {
    const authContext = useContext(AuthContext);
    const logout = () => {
        authContext?.setToken('');
    }
    return {logout};
}

export default useLogout;