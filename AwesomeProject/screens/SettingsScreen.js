import React from 'react';
import { View, Text, StyleSheet, TouchableOpacity, StatusBar } from 'react-native';
import { LinearGradient } from 'expo-linear-gradient';

export default function SettingsScreen() {
  return (
    <View style={styles.container}>
      <LinearGradient
          colors={['#FF7B55', '#C83B14']}
          style={styles.gradient}>
      <View style={styles.statusBar}></View>
      <TouchableOpacity style={styles.button} title="Send Feedback" >
        <Text style={styles.buttonText}>Send Feedback</Text>
      </TouchableOpacity>  
      </LinearGradient>   
    </View>
  );
}

SettingsScreen.navigationOptions = {
  header: null,
};

const styles = StyleSheet.create({
  statusBar: {
    backgroundColor: "#C2185B",
  },
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
  header: {
    backgroundColor: '#F46B45',
  },
  button: {
    backgroundColor: '#EEA849',
    borderRadius: 24,
    padding: 12,
    margin: 96,
  },
  buttonText: {
    color: 'white',
    textAlign: 'center',
    fontSize: 16,
    fontFamily: "Noto Sans Bold"
  }
});
