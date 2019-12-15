import React from 'react';
import { Platform } from 'react-native';
import { createStackNavigator } from 'react-navigation-stack';
import { createBottomTabNavigator } from 'react-navigation-tabs';
import { LinearGradient } from 'expo-linear-gradient';
import TabBarIcon from '../components/TabBarIcon';
import HomeScreen from '../screens/HomeScreen';
import AccountScreen from '../screens/AccountScreen';
import SettingsScreen from '../screens/SettingsScreen';

const config = Platform.select({
  web: { headerMode: 'screen' },
  default: {},
});

//HomeStack
const HomeStack = createStackNavigator(
  {
    Home: HomeScreen,
  },
  config
);

HomeStack.navigationOptions = {
  tabBarLabel: 'Home',
  tabBarIcon: ({ tintColor }) => (
    <TabBarIcon
      tintColor="black" activeTintColor="white"
      name={
        Platform.OS === 'ios'
          ? `ios-home`
          : 'md-home'
      }
    />
  ),
  tabBarOptions: {
    activeTintColor: 'white',
    activeBackgroundColor: '#F46B45',
    labelStyle: {
      fontSize: 12,
      color: 'black',
    },
    style: {
      border: null,
      shadowOffset:{  width: 0,  height: 16,  },
      shadowColor: '#222',
      shadowOpacity: 0.9,
      shadowRadius: 20
    },
    showLabel: false,
  }
};

HomeStack.path = '';

//Account Stack
const AccountStack = createStackNavigator(
  {
    Account: AccountScreen,
  },
  config
);

AccountStack.navigationOptions = {
  tabBarLabel: 'Account',
  tabBarIcon: ({ tintColor }) => (
    <TabBarIcon color={tintColor} name={Platform.OS === 'ios' ? 'ios-person' : 'md-person'} />
  ),
  tabBarOptions: {
    activeTintColor: 'white',
    activeBackgroundColor: '#F46B45',
    labelStyle: {
      fontSize: 12,
      color: 'black',
    },
    style: {
      border: null,
    },
    showLabel: false,
  }

};

AccountStack.path = '';

//settings stack
const SettingsStack = createStackNavigator(
  {
    Settings: SettingsScreen,
  },
  config
);

SettingsStack.navigationOptions = {
  tabBarLabel: 'Settings',
  tabBarIcon: ({ tintColor }) => (
    <TabBarIcon color={tintColor} name={Platform.OS === 'ios' ? 'ios-settings' : 'md-settings'} />
  ),
  tabBarOptions: {
    activeTintColor: 'white',
    activeBackgroundColor: '#F46B45',
    labelStyle: {
      fontSize: 12,
      color: 'black',
    },
    style: {
      border: null,
    },
    showLabel: false,
  }
};

SettingsStack.path = '';


const tabNavigator = createBottomTabNavigator({
  HomeStack,
  AccountStack,
  SettingsStack,
});

tabNavigator.path = '';

export default tabNavigator;
