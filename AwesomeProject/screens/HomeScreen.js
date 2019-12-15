import * as WebBrowser from 'expo-web-browser';
import React from 'react';
import {
  StyleSheet,
  Text,
  View,
  Button,
  StatusBar
} from 'react-native';

export default function HomeScreen() {
  return (
    <View style={styles.container}>
      <StatusBar backgroundColor="blue" barStyle="light-content" />
      <Text>home</Text>     
      <Text>{}</Text>
      <Button title="Deposit"></Button> 
      <Button title="Send"></Button> 
    </View>
  );
}

HomeScreen.navigationOptions = {
  header: null,
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#000000',
  },
});
