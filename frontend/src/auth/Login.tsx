import React, { useContext, useState } from 'react';
import { Container, TextField, Button, Typography, Box } from '@mui/material';
import useLogin from './query/useLogin';
import { AuthContext } from './AuthContextProvider';

function Login() {
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const { mutateAsync: login } = useLogin();
    const authContext = useContext(AuthContext);

    const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
        e.preventDefault();
        try {
            const res = await login({ username, password });
            authContext?.setToken(res.data.access_token);
        } catch (err) {
            return err;
        }
    };

    return (
        <Container maxWidth="sm">
            <Box sx={{ mt: 3 }}>
                <form onSubmit={handleSubmit}>
                <Typography variant="h4" align="center" gutterBottom>
                    Login
                </Typography>
                <TextField
                    label="Username"
                    type="text"
                    fullWidth
                    value={username}
                    onChange={(e) => setUsername(e.target.value)}
                    sx={{ mb: 2 }}
                />
                <TextField
                    label="Password"
                    type="password"
                    fullWidth
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                    sx={{ mb: 2 }}
                />
                <Button type="submit" variant="contained" color="primary" fullWidth>
                    Login
                </Button>
                </form>
            </Box>
        </Container>
    );
}

export default Login;
