import React, { useState } from 'react';
import {
    Card,
    CardContent,
    CardActions,
    IconButton,
    Typography,
    TextField,
    Button,
    Box
} from '@mui/material';
import { ThumbUp, Comment } from '@mui/icons-material';
import { PostType } from '../types';
import CommentList from '../../Comment/components/CommentList';
import useLike from '../query/useLike';
import useLikesCount from '../query/useLikesCount';

interface Props {
    post: PostType;
}
const Post: React.FC<Props> = ({post}) => {
    const [comments, setComments] = useState(post.comments || []);
    const [commentText, setCommentText] = useState('');
    const {data: likesCount} = useLikesCount(post.id);
    const {mutateAsync: likePost} = useLike(post.id);

    const handleLike = async () => {
        try {
            await likePost({id: post.id});
        } catch (err) {
            return err;
        }
    };

    const handleAddComment = async () => {
        // setCommentText('');
    };

    return (
        <Card sx={{ marginBottom: 2 }}>
            <CardContent>
                {/* <Typography variant="h5">{post.title}</Typography> */}
                <Typography variant="h5" color="textSecondary">{post.text}</Typography>
                {post.image_url && <Box component="img" sx={{height: 200, width: 200}} alt='Post image' src={post.image_url}/>}
            </CardContent>
            <CardActions>
                <IconButton onClick={handleLike}>
                    <ThumbUp /> {likesCount?.data ?? 0}
                </IconButton>
                <IconButton>
                    <Comment /> {comments.length}
                </IconButton>
            </CardActions>
            <CardContent>
                <TextField
                    label="Add a comment"
                    fullWidth
                    value={commentText}
                    onChange={(e) => setCommentText(e.target.value)}
                />
                <Button onClick={handleAddComment} variant="contained" color="primary" sx={{ marginTop: 1 }}>
                    Comment
                </Button>
                <CommentList comments={comments} />
            </CardContent>
        </Card>
    );
}

export default Post;
