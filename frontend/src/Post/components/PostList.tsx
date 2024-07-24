import React from 'react';
import { List } from '@mui/material';
import Post from './Post';
import useGetPosts from '../query/useGetPosts';
import LoadingIndicator from '../../common/components/LoadingIndicator';

interface Props {
}
const PostList: React.FC<Props> = () => {
    const {data: posts, isLoading} = useGetPosts({author_ids: [2]});
    if (isLoading || posts == null) {
        return <LoadingIndicator />;
    }

    return (
        <List>
            {posts.data.map((post, index) => (
                <Post key={index} post={post} />
            ))}
        </List>
    );
}

export default PostList;
