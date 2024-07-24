import { AppBar, Toolbar, Typography, Button } from "@mui/material";
import { useContext } from "react";
import { Link } from "react-router-dom";
import { AuthContext } from "../../auth/AuthContextProvider";
import useLogout from "../../hooks/useLogout";

const Navbar = () => {
    const authContext = useContext(AuthContext);
    const {logout} = useLogout();

    return <AppBar position="static">
    <Toolbar>
      <Typography variant="h6" sx={{ flexGrow: 1 }}>
        DiscussHub
      </Typography>
      {authContext?.token ? <Button color="inherit" onClick={logout}>Logout</Button> : <><Button color="inherit" component={Link} to="/signin">Login</Button>
      <Button color="inherit" component={Link} to="/signup">Sign Up</Button></>}
    </Toolbar>
  </AppBar>
}

export default Navbar;