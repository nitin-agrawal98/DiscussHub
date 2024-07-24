import React, { useState } from 'react';
import { Container, TextField, Button, Typography, Box } from '@mui/material';
import useSignup from './query/useSignup';

function Signup() {
    const [name, setName] = useState('');
    const [mobile, setMobile] = useState('');
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [confirmPassword, setConfirmPassword] = useState('');
    const {mutateAsync: signup} = useSignup();

    const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
        e.preventDefault();
        if (password !== confirmPassword) {
            alert("Passwords do not match!");
            return;
        }
        try {
            await signup({name, mobile, email, password});
        alert("Signup successful");
        } catch (err) {
            return err;
        }
    };

    return (
        <Container maxWidth="sm">
            <Box sx={{ mt: 3 }}>
                <form onSubmit={handleSubmit}>
                <Typography variant="h4" align="center" gutterBottom>
                    Sign Up
                </Typography>
                <TextField
                    label="Name"
                    type="text"
                    fullWidth
                    value={name}
                    onChange={(e) => setName(e.target.value)}
                    sx={{ mb: 2 }}
                />
                <TextField
                    label="Mobile"
                    type="text"
                    fullWidth
                    value={mobile}
                    onChange={(e) => setMobile(e.target.value)}
                    sx={{ mb: 2 }}
                />
                <TextField
                    label="Email"
                    type="email"
                    fullWidth
                    value={email}
                    onChange={(e) => setEmail(e.target.value)}
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
                <TextField
                    label="Confirm Password"
                    type="password"
                    fullWidth
                    value={confirmPassword}
                    onChange={(e) => setConfirmPassword(e.target.value)}
                    sx={{ mb: 2 }}
                />
                <Button type="submit" variant="contained" color="primary" fullWidth>
                    Sign Up
                </Button>
                </form>
            </Box>
        </Container>
    );
}

export default Signup;
