import firebase from 'firebase/app'
import 'firebase/auth'
import 'firebase/analytics'
import 'firebase/firestore'


var firebaseConfig = {
    apiKey: "AIzaSyCAfnW9OtwkaGiJDJ1lYvwQeYvFJultjFc",
    authDomain: "chat-app-80766.firebaseapp.com",
    projectId: "chat-app-80766",
    storageBucket: "chat-app-80766.appspot.com",
    messagingSenderId: "1057941999723",
    appId: "1:1057941999723:web:90e10081de8210fbfe212e",
    measurementId: "G-1T546L8ZF9"
  };
  // Initialize Firebase
  firebase.initializeApp(firebaseConfig);
  firebase.analytics();


  const auth = firebase.auth();
  const db = firebase.firestore();

  auth.useEmulator('http://localhost:9099');
  if(window.location.hostname === 'localhost'){
    db.useEmulator('localhost', '8080')
  }

  export {auth, db};
  export default firebase;