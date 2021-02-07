const firebase = require('firebase');

const firebaseConfigWeb = {
	apiKey: "AIzaSyAe2EVtNNEZ8QZ9WKoGkPqFENCsajQeai4",
	authDomain: "conexperto-6b5e7.firebaseapp.com",
	projectId: "conexperto-6b5e7",
	storageBucket: "conexperto-6b5e7.appspot.com",
	messagingSenderId: "473114429364",
	appId: "1:473114429364:web:d46cf4a9838141b3ac54e1",
	measurementId: "G-FXQEXR0HVV"
};
exports.web = firebase.initializeApp(firebaseConfigWeb, 'web');


const firebaseConfigAdmin = {
	apiKey: "AIzaSyD4uyFMfi35s6nae3gjZfB_Wd1hMmNF7_w",
	authDomain: "conexperto-admin.firebaseapp.com",
	projectId: "conexperto-admin",
	storageBucket: "conexperto-admin.appspot.com",
	messagingSenderId: "40989086504",
	appId: "1:40989086504:web:e2035160b51bcc9089b61d",
	measurementId: "G-DG3JG3635L"
};
exports.admin = firebase.initializeApp(firebaseConfigAdmin, 'admin');

