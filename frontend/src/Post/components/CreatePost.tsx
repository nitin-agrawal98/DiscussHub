import React, { useState } from 'react';
import { TextField, Button, Box } from '@mui/material';

interface Props {}
const CreatePost: React.FC<Props> = ({}) => {
    const [title, setTitle] = useState('');
    const [content, setContent] = useState('');

    const handleSubmit = (e: React.FormEvent<HTMLFormElement>) => {
        e.preventDefault();
        const newPost = { title, content, likes: 0, comments: [] };
        // addPost(newPost);
        setTitle('');
        setContent('');
    };

    return (
        <Box component="form" onSubmit={handleSubmit} sx={{ marginBottom: 3 }}>
            <TextField
                label="Title"
                fullWidth
                value={title}
                onChange={(e) => setTitle(e.target.value)}
                sx={{ marginBottom: 2 }}
            />
            <TextField
                label="Content"
                fullWidth
                multiline
                rows={4}
                value={content}
                onChange={(e) => setContent(e.target.value)}
                sx={{ marginBottom: 2 }}
            />
            <Button type="submit" variant="contained" color="primary">
                Post
            </Button>
        </Box>
    );
}

export default CreatePost;
