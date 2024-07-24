import React from 'react';
import { List } from '@mui/material';
import { CommentType } from '../types';
import Comment from './Comment';

interface Props {
    comments: CommentType[];
}
const CommentList: React.FC<Props> = ({ comments }) => {
    return (
        <List>
            {comments.map(comment => (
                <Comment key={comment.id} comment={comment} />
            ))}
        </List>
    );
}

export default CommentList;
