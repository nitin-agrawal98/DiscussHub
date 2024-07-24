import { CommentType } from "../../Comment/types";

export interface PostType {
    id: number;
    title: string;
    image_url?: string;
    text: string;
    likes_count: number;
    comments: CommentType[];
}