import queryString from 'query-string';
import config from "../../config/config"
import { get, post, uploadFile } from "../../services/api"
import { PostType } from '../types';
import { CreatePostPayload, GetPostPayload, GetPostsPayload, LikePayload, LikesCountResponse } from './types';

export const getPosts = async (payload: GetPostsPayload, token: string) => {
    try {
    return await get<PostType[]>(`${config.discussion_service_url}authors?${queryString.stringify({"author_ids": payload.author_ids.join(',')})}`, token);
    } catch (err) {
        return Promise.reject(err);
    }
}

export const addPost = async (data: CreatePostPayload, token: string) => {
    try {
        return await uploadFile(config.discussion_service_url, data, token);
    } catch (err) {
        return Promise.reject(err);
    }
}

export const getPost = async (payload: GetPostPayload, token: string) => {
    try {
        return await get<PostType>(`${config.discussion_service_url}${payload.id}`, token);
    } catch (err) {
        return Promise.reject(err);
    }
}

export const getLikesCount = async (payload: LikePayload, token: string) => {
    try {
        return await get<LikesCountResponse>(`${config.discussion_service_url}${payload.id}/like`, token);
    } catch (err) {
        return Promise.reject(err);
    }
}

export const likePost = async (payload: LikePayload, token: string) => {
    try {
        return await post(`${config.discussion_service_url}${payload.id}/like`, {}, token);
    } catch (err) {
        return Promise.reject(err);
    }
}