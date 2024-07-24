import { useMutation } from "react-query";
import { LoginPayload, LoginResponse } from "../api/types";
import { login } from "../api";

const useLogin = () => {
    return useMutation<LoginResponse, unknown, LoginPayload>({
        mutationFn: async (payload) => {
            try {
                return await login(payload);
            } catch (err) {
                return Promise.reject(err);
            }
        }
    });
}

export default useLogin;