import axios from 'axios';
import { LoginPayload, SignupPayload } from './types';
import config from '../../config/config';

export const login = async (payload: LoginPayload) => {
    try {
        console.log(config.host);
        const res = await axios.post(`${config.host}login`, {}, {
            auth: payload
        });
        return res.data;
    } catch (err) {
        return Promise.reject(err);
    }
}

export const signup = async (data: SignupPayload) => {
    try {
        const res = await axios.post(`${config.host}signup`, data);
        return res.data;
    } catch (err) {
        return Promise.reject(err);
    }
}