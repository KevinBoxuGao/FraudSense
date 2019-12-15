import * as WebBrowser from 'expo-web-browser';
import React from 'react';
import {
  StyleSheet,
  Text,
  View,
  TouchableOpacity,
  StatusBar
} from 'react-native';
import { withOrientation } from 'react-navigation';
import { LinearGradient } from 'expo-linear-gradient';

export default function HomeScreen() {
  return (
    <View style={styles.container}>  
     <LinearGradient
          colors={['#FF7B55', '#C83B14']}
          style={styles.gradient}>
        <Text style={styles.dollarAmount}>36.46 USD</Text>
        <View style={styles.buttonGroup}>
          <TouchableOpacity style={styles.button} title="Deposit">
            <Text style={styles.buttonText}>Deposit</Text>
          </TouchableOpacity> 
          <TouchableOpacity style={styles.button}>
            <Text style={styles.buttonText}>Send</Text>
          </TouchableOpacity> 
        </View>
      </LinearGradient>
    </View>
  );
}

HomeScreen.navigationOptions = {
  header: null,
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#F46B45',
    padding: 30,
    justifyContent: 'center',
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
  dollarAmount: {
    fontSize: 42,
    alignSelf: 'center',
    color: 'white',
    fontFamily: 'Noto Sans Bold'
  },
  buttonGroup: {
    flexDirection: 'row',
    justifyContent: 'center',
  },
  button: {
    backgroundColor: '#EEA849',
    borderRadius: 16,
    padding: 8,
    margin: 10,
    width: 120,
  },
  buttonText: {
    color: 'white',
    textAlign: 'center',
    fontFamily: "Noto Sans Bold",
    fontSize: 14
  }
});
