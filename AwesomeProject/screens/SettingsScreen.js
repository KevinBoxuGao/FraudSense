import React from 'react';
import { View, Text, StyleSheet } from 'react-native';

export default function SettingsScreen() {
  return (
    <View>
      <Text>settings</Text>
    </View>
  );
}

SettingsScreen.navigationOptions = {
  title: 'app.json',
};
