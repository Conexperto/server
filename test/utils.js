exports.login = async function(email, password, app) {
	try {
		const user_record = await app.auth().signInWithEmailAndPassword(email, password);

		return await app.auth().currentUser.getIdToken();
	}
	catch(err) {
		console.log(err)
	}
}
