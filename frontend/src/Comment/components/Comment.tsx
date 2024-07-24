import React from 'react';
import { ListItem, ListItemText } from '@mui/material';
import { CommentType } from '../types';

interface Props {
    comment: CommentType;
}
const Comment: React.FC<Props> = ({ comment }) => {
    return (
        <ListItem>
            <ListItemText primary={comment.text} />
        </ListItem>
    );
}

export default Comment;
