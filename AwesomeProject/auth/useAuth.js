import React, { useState, useEffect } from 'react';
import {withFirebase} from '../firebase';

const useAuth = () => {
  const [state, setState] = React.useState(() => {    
    const user = props.firebase.auth().currentUser    
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
    const unsubscribe = this.props.firebase.auth().onAuthStateChange(onChange)
    // unsubscribe to the listener when unmounting
    return () => unsubscribe()
  }, [])

  return state
}

export default withFirebase(useAuth);