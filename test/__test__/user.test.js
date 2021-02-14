const request = require('supertest');
const { admin } = require('../config');
const { login } = require('../utils');


const domain = "http://api:3000/api/v1";

jest.setTimeout(100000)

describe("User", () => {
	let token_admin = null, token = null, uid = null;

	beforeAll(async () => {
		token = await login('conexpertotesting@gmail.com', 
							'conexpertotesting2021', admin);
	});

	describe("POST /user", () => {
		test("It should create an user", async () => {
			const response = await request(domain)
										.post('/user')
										.set('Authorization', 'Bearer ' + token_admin)
										.send({
											display_name: 'frfernandezdev',
											email: 'frfernandezdev@gmail.com',
											password: 'token.01',
											phone_number: '+10000000000',
											name: 'Fernando',
											lastname: 'Fernandez',
											headline: 'Lorem ipsum',
											about_me: 'Lorem ipsum'
										});
			//if (response.error) {
			//	console.log(response.error);
			//}
			expect(response.statusCode).toBe(200);
			uid = response.body.response.uid;
		});

		test("It should create a repeating user and response with error 400 ", async () => {
			const response = await request(domain)
										.post('/user')
										.set('Authorization', 'Bearer ' + token_admin)
										.send({
											display_name: 'frfernandezdev',
											email: 'frfernandezdev@gmail.com',
											password: 'token.01',
											phone_number: '+10000000000',
											name: 'Fernando',
											lastname: 'Fernandez',
											headline: 'Lorem ipsum',
											about_me: 'Lorem ipsum'
										});
			//if (response.error) {
			//	console.log(response.error);
			//}
			expect(response.statusCode).toBe(400);
		});

		test("It should create a user, but without some fields and response with error 400", async () => {
			const response = await request(domain)
										.post('/user')
										.set('Authorization', 'Bearer ' + token_admin)
										.send({
											email: 'frfernandezdev@gmail.com'
										});
			//if (response.error) {
			//	console.log(response.error);
			//}
			expect(response.statusCode).toBe(400);
		});

		test("It should create a user, but with some extra fields and response with error 400", async () => {
			const response = await request(domain)
										.post('/user')
										.set('Authorization', 'Bearer ' + token_admin)
										.send({
											email: 'frfernandezdev@gmail.com',
											passport: 'ABC1235598A'
										});
			//if (response.error) {
			//	console.log(response.error);
			//}
			expect(response.statusCode).toBe(400);
		});

		afterAll(async () => {
			token = await login('frfernandezdev@gmail.com', 
								'token.01', admin);
		});
	});

	describe("GET /user", () => {
		test("it should respond with an data user", async () => {
			const response = await request(domain)
										.get('/user/' + uid)
										.set('Authorization', 'Bearer ' + token)
		
			expect(response.statusCode).toBe(200);
		});

		test("it should respond with an error 400, because not send authorization headers", async () => {
			const response = await request(domain)
										.get('/user/' + uid);

			expect(response.statusCode).toBe(400);
		});

		test("it should respond with an error 400, because send invalid format authorization headers without bearer", async () => {
			const response = await request(domain)
										.get('/user/' + uid)
										.set('Authorization', token);

			expect(response.statusCode).toBe(400);
		});

		test("it should respond with an error 400, because send invalid format authorization headers with without idtoken", async () => {
			const response = await request(domain)
										.get('/user/' + uid)
										.set('Authorization', 'Bearer');

			expect(response.statusCode).toBe(400);
		});
	});

	describe("PUT /user", () => {
		test("It should updated an user", async () => {
			const response = await request(domain)
										.put('/user/' + uid)
										.set('Authorization', 'Bearer ' + token)
										.send({
											phone_number: '+10000000000',
											name: 'Fernando',
											lastname: 'Fernandez'
										});
			if (response.error) {
				console.log(response.error)
			}
			expect(response.statusCode).toBe(200);
		});
	});

	describe("PATCH /user", () => {
		test("It should updated an user", async () => {
			const response = await request(domain)
										.patch('/user/' + uid)
										.set('Authorization', 'Bearer ' + token)
										.send({
											display_name: 'frfernandezdev1996'
										});
			if (response.error) {
				console.log(response.error)
			}
			expect(response.statusCode).toBe(200);
		});
	});

	describe("PATCH /user/disabled", () => {
		test("It should disabled an user", async () => {
			const response = await request(domain)
										.patch('/user/disabled/' + uid)
										.set('Authorization', 'Bearer ' + token);
			if (response.error) {
				console.log(response.error)
			}
			expect(response.statusCode).toBe(200);
		});
	});

	afterAll(async () => {
		const response = await request(domain)
									.delete('/user/' + uid)
									.set('Authorization', 'Bearer ' + token);
		if (response.error) {
			console.log(response.error)
		}
	});
});
