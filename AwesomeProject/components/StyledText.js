import React from 'react';
import { Text } from 'react-native';

export function NotoSansBold(props) {
  return (
    <Text {...props} style={[props.style, { fontFamily: 'Noto Sans Bold' }]} />
  );
}
