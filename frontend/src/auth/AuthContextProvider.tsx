import { createContext, PropsWithChildren, SetStateAction, useEffect, useState } from "react";
import { TOKEN } from "../constants/localstorage";

export interface AuthContextType {
    token: string | null;
    setToken: React.Dispatch<SetStateAction<string>>;
}
export const AuthContext = createContext<AuthContextType | null>(null);

interface Props extends PropsWithChildren {}
export const AuthContextProvider: React.FC<Props> = ({children}) => {
    const [token, setToken] = useState(localStorage.getItem(TOKEN) ?? '');

    useEffect(() => {
        if (token) {
            localStorage.setItem(TOKEN, token);
        } else {
            localStorage.removeItem(TOKEN);
        }
    }, [token])

    return <AuthContext.Provider value={{token, setToken}}>{children}</AuthContext.Provider>
};