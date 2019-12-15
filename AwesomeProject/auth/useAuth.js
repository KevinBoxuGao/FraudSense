import React, { useState, useEffect } from 'react';
import {f, auth} from '../firebase/config';

const useAuth = () => {
  const [state, setState] = React.useState(() => {    
    const user = f.auth().currentUser    
    return {      
      initializing: !user,      
      user,    
    } 
  })
  
  function onChange(user) {
    setState({ initializing: false, user })
  }

  React.useEffect(() => {
    // listen for auth state changes
    const unsubscribe = f.auth().onAuthStateChanged(onChange)
    // unsubscribe to the listener when unmounting
    return () => unsubscribe()
  }, [])

  return state
}

export default useAuth;