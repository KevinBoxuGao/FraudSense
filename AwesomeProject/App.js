import { AppLoading } from 'expo';
import React, { useState } from 'react';
import { Platform, StatusBar, StyleSheet, View, Text } from 'react-native';
import { Ionicons } from '@expo/vector-icons';
import { NotoSansBold } from './components/StyledText.js';
import * as Font from 'expo-font';
import AppNavigator from './navigation/AppNavigator';
import LoginNavigator from './auth/LoggingContainer';
import useAuth from './auth/useAuth';

export default function App(props) {
  const [isLoadingComplete, setLoadingComplete] = useState(false);

  const { initializing, user } = useAuth();

  if (!isLoadingComplete && !props.skipLoadingScreen) {
    return (
      <AppLoading
        startAsync={loadResourcesAsync}
        onError={handleLoadingError}
        onFinish={() => handleFinishLoading(setLoadingComplete)}
      />
    );
  } else {
    console.log(user);
    return (
      <View style={styles.container}>
        {Platform.OS === 'ios' && <StatusBar barStyle="default" />}
        {user ? <AppNavigator />: <LoginNavigator />}
      </View>
    );
  }
} 



async function loadResourcesAsync() {
  await Promise.all([
    
    //Asset.loadAsync([
    //  require('./assets/images/default-profile.png'),
    //]),
    
    Font.loadAsync({
      // This is the font that we are using for our tab bar
      ...Ionicons.font,
      // We include SpaceMono because we use it in HomeScreen.js. Feel free to
      // remove this if you are not using it in your app
      'Noto Sans Regular': require('./assets/fonts/NotoSans-Regular.ttf'),
      'Noto Sans Bold': require('./assets/fonts/NotoSans-Bold.ttf'),
    }),
    console.log('assets loaded')
  ]);
}

function handleLoadingError(error) {
  // In this case, you might want to report the error to your error reporting
  // service, for example Sentry
  console.warn(error);
}

function handleFinishLoading(setLoadingComplete) {
  setLoadingComplete(true);
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#fff',
  },
});
