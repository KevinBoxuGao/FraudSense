import LoginScreen from './LoginScreen';
import SignUpScreen from './SignUpScreen';
import {createStackNavigator} from 'react-navigation-stack';
import {createAppContainer} from 'react-navigation';

const LoginNavigator = createStackNavigator(
    {
        Login: LoginScreen,
        SignUp: SignUpScreen,
    },
    {
        initialRouteName: 'Login',
        header: null,
        headerMode: 'none',
    },
);


export default createAppContainer(LoginNavigator);

