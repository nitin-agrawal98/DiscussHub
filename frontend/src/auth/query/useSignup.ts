import { useMutation } from "react-query";
import { SignupPayload, SignupResponse } from "../api/types";
import { signup } from "../api";

const useSignup = () => {
    return useMutation<SignupResponse, unknown, SignupPayload>({
        mutationFn: async (payload) => {
            try {
                return await signup(payload);
            } catch (err) {
                return Promise.reject(err);
            }
        }
    });
}

export default useSignup;