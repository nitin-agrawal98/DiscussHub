import axios from "axios";
import config from "../config/config";

const getHeaders = (token: string) => {
    return {
        'Content-type': 'application/json',
        'Authorization': `Bearer ${token}`,
    }
}

export const get = async <T>(url: string, token: string): Promise<T> => {
    try {
        const headers = getHeaders(token);
        const res = await axios.get(config.host + url, { headers });
        return res.data;
    } catch (err) {
        return Promise.reject(err);
    }
};

export const post = async <T>(url: string, body: T, token: string) => {
    try {
        const headers = getHeaders(token);
        const res = await axios.post(config.host + url, body, { headers });
        return res.data;
    } catch (err) {
        return Promise.reject(err);
    }
}

export const uploadFile = async (url: string, body: { [key: string]: any }, token: string) => {
    try {
        const headers = {...getHeaders(token), 'Content-type': 'multipart/form-data;'};
        const formData = new FormData();
        Object.keys(body).forEach(key => formData.append(key, body[key] as string | Blob));
        const res = await axios.post(config.host + url, body, { headers });
        return res.data;
    } catch (err) {
        return Promise.reject(err);
    }
}