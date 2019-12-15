import app from 'firebase/app'
import 'firebase/auth';

const config = {
  apiKey: "AIzaSyAjdId9pkfkA6tOMM7Iwdfex-72FT1juU4",
  authDomain: "hack-the-hammer-92b8f.firebaseapp.com",
  databaseURL: "https://hack-the-hammer-92b8f.firebaseio.com",
  projectId: "hack-the-hammer-92b8f",
  storageBucket: "hack-the-hammer-92b8f.appspot.com",
  messagingSenderId: "411828411394",
  appId: "1:411828411394:web:e85506ae71fdd8bc4ddb1b",
  measurementId: "G-PXYGNLVX9H"
};

class Firebase {
  constructor() {
    app.initializeApp(config);
    this.auth = app.auth();
    this.doCreateUserWithEmailAndPassword = this.doCreateUserWithEmailAndPassword.bind(this);
  }

  doCreateUserWithEmailAndPassword(email, password, displayName) {
    this.auth.createUserWithEmailAndPassword(email, password).then(
      (success) => {
        success.updateProfile({
          displayName: displayName
        })
      }
    )
  }
  
  doSignInWithEmailAndPassword = (email, password) => 
  this.auth.signInWithEmailAndPassword(email, password);
  doSignOut = () => this.auth.signOut();
  doPasswordReset = email => this.auth.sendPasswordResetEmail(email);
  doPasswordUpdate = password =>
  this.auth.currentUser.updatePassword(password);
}

export default Firebase;