import React, { useState } from 'react'
import { View, Text, Button, TextInput,  StyleSheet, StatusBar, Alert } from 'react-native';
import {withFirebase} from '../firebase';
import ErrorBoundary from '../testing/ErrorBoundary';

function LoginScreen(props) {
    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");
    const [errorStatus, setError] = useState(false);

    const login = () => {
        console.log(props);
        props.firebase
            .doSignInWithEmailAndPassword(email, password)
            .catch(error => {
                console.log(error);
                setError(true);
                Alert.alert(
                    'Alert Title',
                    'My Alert Msg',
                    [
                      {text: 'Ask me later', onPress: () => console.log('Ask me later pressed')},
                      {
                        text: 'Cancel',
                        onPress: () => console.log('Cancel Pressed'),
                        style: 'cancel',
                      },
                      {text: 'OK', onPress: () => console.log('OK Pressed')},
                    ],
                    {cancelable: false},
                );
            });
        event.preventDefault();
    }

    return (
        <ErrorBoundary>
        <View>
            <StatusBar barStyle = "dark-content" hidden = {false} backgroundColor = "#00BCD4" translucent = {true}/>
            <Text>Log In</Text>
            <View>
                <Text>Email</Text> 
                <TextInput 
                    style={styles.input} 
                    name="email"
                    placeholder="email"
                    onChangeText={(email) => setEmail(email)}
                    value={email}
                >
                </TextInput>
            </View>
            <View>
                <Text>Password</Text> 
                <TextInput              
                    style={styles.input} 
                    name="password"
                    placeholder="password"
                    onChangeText={(password) => setPassword(password)}
                    value={password}
                ></TextInput>
            </View>
            <Button title="Login" onPress={() => login()}/>
            {errorStatus && <Text style={{ color: 'red' }}>
            {errorStatus}
            </Text>}
        </View>
        </ErrorBoundary>
    );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    paddingTop: 15,
    backgroundColor: '#fff',
  },
  input: {
    borderWidth: 1,
  }
});

export default withFirebase(LoginScreen);
