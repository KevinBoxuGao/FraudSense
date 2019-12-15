import React from 'react';
import { Text, View, StyleSheet, TouchableOpacity, Image } from 'react-native';
import {withFirebase} from '../firebase';
import { LinearGradient } from 'expo-linear-gradient';
import {f, auth} from '../firebase/config';

export default function AccountScreen() {
  return (
    <View style={styles.container}>
      <View style={styles.user}>
        <Text>{f.auth().currentUser.email}</Text>
      </View>
      <View style={styles.group}>
      <TouchableOpacity style={styles.button} title="Sign Out" onPress={() => f.auth().signOut()}>
        <Text style={styles.buttonText}>Sign Out</Text>
      </TouchableOpacity>  
      <TouchableOpacity style={styles.button} title="Change Password" onPress={() => console.log('yes')}>
        <Text style={styles.buttonText}>Change Password</Text>
      </TouchableOpacity>  
      </View>
    </View>
  );
}

//onClick={() => this.props.firebase.doSignOut()}

AccountScreen.navigationOptions = {
  title: 'Account',
};

const styles = StyleSheet.create({
  user: {
    backgroundColor: 'white',
    padding: 30,
    borderWidth: 0.5,
    borderColor: '#c4c4c4',
    alignContent: 'center',
    marginBottom: 20,
    borderTopWidth: 0,
  },
  container: {
    flex: 1,
    backgroundColor: '#EFEFEF',
  },
  header: {
    backgroundColor: '#F46B45',
  },
  group: {
    borderBottomWidth: 0.5,
    borderColor: '#c4c4c4',
  },
  button: {
    backgroundColor: 'white',
    padding: 12,
    paddingLeft: 30,
    borderTopWidth: 0.5,
    borderColor: '#c4c4c4',
  },
  buttonText: {
    color: 'black',
    textAlign: 'left',
    fontFamily: "Noto Sans Regular"
  }
});