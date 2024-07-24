import { Routes, Route, Navigate } from 'react-router-dom';
import Login from './auth/Login';
import Signup from './auth/Signup';
import AuthenticatedRoute from './route-wrappers/AuthenticatedRoute';
import UnauthenticatedRoute from './route-wrappers/UnauthenticatedRoute';
import PostList from './Post/components/PostList';
import Navbar from './common/components/NavBar';

const App = () => {
  return (
    <div>
      <Navbar />
      <Routes>
        <Route element={<UnauthenticatedRoute />}>
          <Route path="/signup" element={<Signup />} />
          <Route path="/signin" element={<Login />} />
        </Route>
        <Route element={<AuthenticatedRoute />}>
          <Route path='/' element={<Navigate to='/home' />} />
          <Route path='/home' element={<PostList />} />
        </Route>
      </Routes>
    </div>
  );
}

export default App;
