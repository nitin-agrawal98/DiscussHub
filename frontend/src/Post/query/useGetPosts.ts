import { useQuery } from "react-query";
import { POSTS } from "./keys";
import { useContext } from "react";
import { AuthContext } from "../../auth/AuthContextProvider";
import { getPosts } from "../api";
import { GetPostsPayload } from "../api/types";
import { PostType } from "../types";

const useGetPosts = ({author_ids}: GetPostsPayload) => {
    const authContext = useContext(AuthContext);

    return useQuery<unknown, unknown, {data: PostType[]}>({
        queryKey: [POSTS],
        queryFn: async () => await getPosts({author_ids}, authContext?.token ?? ''),
        enabled: authContext?.token !== '',
        initialData: {data: []},
    });
}

export default useGetPosts;