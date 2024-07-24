export interface LoginPayload {
    username: string;
    password: string;
}

export interface LoginResponse {
    data: {
        access_expires_on: string;
        access_token: string;
        refresh_expires_on:  string;
        refresh_token: string;
    }
}

export interface SignupPayload {
    name: string;
    email: string;
    mobile: string;
    password: string;
}

export interface SignupResponse {
    data: Omit<SignupPayload, 'password'> & {id: number}
}