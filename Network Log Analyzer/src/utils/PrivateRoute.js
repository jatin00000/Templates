import { Route, useNavigate } from 'react-router-dom'
import { useContext } from 'react'
import AuthContext from '../context/AuthContext'

const PrivateRoute = ({children, ...rest}) => {
    let {user} = useContext(AuthContext)
    const navigate = useNavigate();
    return(
        <Route element={!user ? navigate('/login') :   children} {...rest}></Route>
    )
}

export default PrivateRoute;