export type GetPostsPayload = {author_ids: number[]};
export type GetPostPayload = {id: number};

export type CreatePostPayload = {
    text: string;
    image: File;
};

export type LikePayload = {id: number};

export type LikesCountResponse = {data: number};