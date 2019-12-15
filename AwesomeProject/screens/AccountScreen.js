import React from 'react';
import { Text, View, StyleSheet, Button } from 'react-native';
import {withFirebase} from '../firebase';

function AccountScreen() {
  return (
    <View style={styles.container}>
      <Text>account</Text>
      <Button title="Sign Out" />      
    </View>
  );
}

//onClick={() => this.props.firebase.doSignOut()}

AccountScreen.navigationOptions = {
  title: 'Account',
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    paddingTop: 15,
    backgroundColor: '#fff',
  },
});

export default withFirebase(AccountScreen);