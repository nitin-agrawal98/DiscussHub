import { useMutation, useQueryClient } from "react-query";
import { LikePayload } from "../api/types";
import { useContext } from "react";
import { AuthContext } from "../../auth/AuthContextProvider";
import { likePost } from "../api";
import { LIKES_COUNT, POSTS } from "./keys";

const useLike = (id: number) => {
    const authContext = useContext(AuthContext);
    const queryClient = useQueryClient();
    return useMutation<unknown, unknown, LikePayload>({
        mutationFn: async ({id}) => {
            try {
                return await likePost({id}, authContext?.token ?? '');
            } catch (err) {
                return err;
            }
        },
        onSuccess: () => {
            queryClient.invalidateQueries({queryKey: [LIKES_COUNT, id]});
        }
    });
}

export default useLike;