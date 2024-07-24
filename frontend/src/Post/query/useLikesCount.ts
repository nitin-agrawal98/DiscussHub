import { useQuery } from "react-query";
import { useContext } from "react";
import { AuthContext } from "../../auth/AuthContextProvider";
import { getLikesCount } from "../api";
import { LIKES_COUNT } from "./keys";
import { LikesCountResponse } from "../api/types";

const useLikesCount = (id: number) => {
    const authContext = useContext(AuthContext);
    return useQuery<unknown, unknown, LikesCountResponse>({
        queryKey: [LIKES_COUNT, id],
        queryFn: () => getLikesCount({id}, authContext?.token ?? '')
    });
}

export default useLikesCount;