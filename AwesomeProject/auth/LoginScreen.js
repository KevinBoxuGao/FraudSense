import React, { useState } from 'react'
import { View, Text, TouchableOpacity, TextInput,  StyleSheet, Keyboard, TouchableWithoutFeedback, KeyboardAvoidingView } from 'react-native';
import {f, auth} from '../firebase/config';
import { LinearGradient } from 'expo-linear-gradient';

function LoginScreen(props) {

    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");
    const [errorStatus, setError] = useState(null);

    const login = () => {
        f.auth().signInWithEmailAndPassword(email, password)
            .catch(error => {
              console.log(error);
              setError(error);
            });
    }

    return (
      
        <TouchableWithoutFeedback onPress={Keyboard.dismiss} accessible={false}>
          
            <KeyboardAvoidingView
            style={styles.container}
            behavior="padding"
            >
              
                <View style={styles.container}>
                <LinearGradient
                  colors={['#FF7B55', '#C83B14']}
                  style={styles.gradient}>
                    <View style={styles.formContainer}> 
                    <Text style={styles.title}>Log In</Text>
                    <View>
                        <Text style={styles.inputTitle} >Email</Text> 
                        <TextInput 
                            style={styles.input} 
                            name="email"
                            placeholder="block@chain.org"
                            onChangeText={(email) => setEmail(email)}
                            value={email}
                        >
                        </TextInput>
                    </View>
                    <View>
                        <Text style={styles.inputTitle}>Password</Text> 
                        <TextInput              
                            style={styles.input} 
                            name="password"
                            placeholder="anything but 1234"
                            secureTextEntry={true}
                            onChangeText={(password) => setPassword(password)}
                            value={password}
                        ></TextInput>
                    </View>
                      <TouchableOpacity title="Login" style={styles.button} onPress={() => login()}>
                          <Text style={styles.buttonText}>Login</Text>
                      </TouchableOpacity>
                      <TouchableOpacity title="SignUp" style={styles.button, styles.signup} onPress={() => props.navigation.navigate('SignUp')}>
                          <Text style={styles.buttonText}>Sign Up</Text>
                      </TouchableOpacity>
                      <Text>{errorStatus}</Text>
                      
                    </View>
                    </LinearGradient>
                </View>
                
            </KeyboardAvoidingView>
            
        </TouchableWithoutFeedback>
        
    );
}

const styles = StyleSheet.create({
  container: {
    position: 'absolute',
    top: 0,
    right: 0,
    bottom: 0,
    left: 0,
    flex: 1,
    justifyContent: 'center',
  },
  title: {
    fontSize: 24,
    color: 'white',
    alignSelf: 'center',
    margin: 15,
    fontFamily: "Noto Sans Bold"
  },
  inputTitle: {
    color: '#FAFAFA',
    margin: 5,
    fontFamily: "Noto Sans Bold",
    width: 250,
    alignSelf: "center"
  },
  gradient: {
    position: 'absolute',
    top: 0,
    right: 0,
    bottom: 0,
    left: 0,
    flex: 1,
    justifyContent: 'center',
  },
  input: {
    borderWidth: 1,
    borderColor: '#FFFFFF',
    color: 'black',
    backgroundColor: '#e8e8e8',
    borderRadius: 20,
    padding: 6,
    width: 250,
    alignSelf: "center",
    fontFamily: "Noto Sans Regular"
  },
  button: {
    backgroundColor: '#EEA849',
    borderRadius: 20,
    marginTop: 25,
    padding: 8,
    textAlign: 'center',
    marginBottom: 30,
    width: 100,
    alignSelf: "center"
  },
  buttonText: {
    color: '#FAFAFA',
    fontFamily: 'Noto Sans Bold',
    textAlign: 'center'
  },
  signup: {
    marginTop: -10
  }
});

export default LoginScreen;
