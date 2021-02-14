const request = require('supertest');
const { web } = require('../config');
const { login } = require('../utils');


const domain = "http://api:3000/api/v1";

jest.setTimeout(100000)

describe("Auth", () => {
	let token = null;
	
	describe("POST /auth", () => {
		test("It should create an user", async () => {
			const response = await request(domain)
										.post('/auth')
										.send({
											email: 'frfernandezdev@gmail.com',
											password: 'token.01',
											display_name: 'frfernandezdev'
										});
			//if (response.error) {
			//	console.log(response.error);
			//}
			expect(response.statusCode).toBe(200);
		});

		test("It should create a repeating user and response with error 400 ", async () => {
			const response = await request(domain)
										.post('/auth')
										.send({
											email: 'frfernandezdev@gmail.com',
											password: 'token.01',
											display_name: 'frfernandezdev'
										});
			//if (response.error) {
			//	console.log(response.error);
			//}
			expect(response.statusCode).toBe(400);
		});

		test("It should create a user, but without some fields and response with error 400", async () => {
			const response = await request(domain)
										.post('/auth')
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
										.post('/auth')
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
								'token.01', web);
		});
	});

	describe("GET /auth", () => {
		test("It should respond with an data user", async () => {
			const response = await request(domain)
										.get('/auth')
										.set('Authorization', 'Bearer ' + token);
			//if (response.error) {
			//	console.log(response.error)
			//}
			expect(response.statusCode).toBe(200);
		});

		test("It should respond with an error 400, because not send authorization headers", async () => {
			const response = await request(domain)
										.get('/auth');
			//if (response.error) {
			//	console.log(response.error)
			//}
			expect(response.statusCode).toBe(400);
		});

		test("It should respond with an error 400, because send invalid format authorization headers without bearer", async () => {
			const response = await request(domain)
										.get('/auth')
										.set('Authorization', token);
			//if (response.error) {
			//	console.log(response.error)
			//}
			expect(response.statusCode).toBe(400);
		});

		test("It should respond with an error 400, because send invalid format authorization headers with Bearer and without idtoken", async () => {
			const response = await request(domain)
										.get('/auth')
										.set('Authorization', 'Bearer');
			//if (response.error) {
			//	console.log(response.error)
			//}
			expect(response.statusCode).toBe(400);
		});
	});

	describe("PUT /auth", () => {
		test("It should updated an user", async () => {
			const response = await request(domain)
										.put('/auth')
										.set('Authorization', 'Bearer ' + token)
										.send({
											phone_number: '+10000000000',
											name: 'Fernando',
											lastname: 'Fernandez',
											headline: 'Lorem ipsum',
											about_me: 'Lorem ipsum'
										});
			if (response.error) {
				console.log(response.error)
			}
			expect(response.statusCode).toBe(200);
		});
	});

	describe("PATCH /auth", () => {
		test("It should updated an user", async () => {
			const response = await request(domain)
										.patch('/auth')
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

	//describe("PATCH /auth/disabled", () => {
	//	test("It should disabled an user", async () => {
	//		const response = await request(domain)
	//									.patch('/auth/disabled')
	//									.set('Authorization', 'Bearer ' + token);
	//		if (response.error) {
	//			console.log(response.error)
	//		}
	//		expect(response.statusCode).toBe(200);
	//	});

	//	afterAll(async () => {
	//		const response = await request(domain)
	//									.patch('/auth/disabled')
	//									.set('Authorization', 'Bearer ' + token);
	//		if (response.error) {
	//			console.log(response.error)
	//		}
	//	})
	//});

	afterAll(async () => {
		const response = await request(domain)
									.delete('/auth')
									.set('Authorization', 'Bearer ' + token);
		if (response.error) {
			console.log(response.error)
		}
	});
});

