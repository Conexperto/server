const request = require('supertest');
const { admin } = require('../config');
const { login } = require('../utils');


const domain = "http://api:3000/api/v1";

jest.setTimeout(100000)

describe("AuthAdmin", () => {
	let token = null;

	describe("POST /admin/auth", () => {
		test("It should create an user admin", async () => {
			const response = await request(domain)
										.post('/admin/auth')
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

		test("It should create a repeating user admin and response with error 400 ", async () => {
			const response = await request(domain)
										.post('/admin/auth')
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

		test("It should create a user admin, but without some fields and response with error 400", async () => {
			const response = await request(domain)
										.post('/admin/auth')
										.send({
											email: 'frfernandezdev@gmail.com'
										});
			//if (response.error) {
			//	console.log(response.error);
			//}
			expect(response.statusCode).toBe(400);
		});

		test("It should create a user admin, but with some extra fields and response with error 400", async () => {
			const response = await request(domain)
										.post('/admin/auth')
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

	describe("GET /admin/auth", () => {
		test("it should respond with an data user admin", async () => {
			const response = await request(domain)
										.get('/admin/auth')
										.set('Authorization', 'Bearer ' + token)
		
			expect(response.statusCode).toBe(200);
		});

		test("it should respond with an error 400, because not send authorization headers", async () => {
			const response = await request(domain)
										.get('/admin/auth');

			expect(response.statusCode).toBe(400);
		});

		test("it should respond with an error 400, because send invalid format authorization headers without bearer", async () => {
			const response = await request(domain)
										.get('/admin/auth')
										.set('Authorization', token);

			expect(response.statusCode).toBe(400);
		});

		test("it should respond with an error 400, because send invalid format authorization headers with without idtoken", async () => {
			const response = await request(domain)
										.get('/admin/auth')
										.set('Authorization', 'Bearer');

			expect(response.statusCode).toBe(400);
		});
	});

	describe("PUT /admin/auth", () => {
		test("It should updated an user admin", async () => {
			const response = await request(domain)
										.put('/admin/auth')
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

	describe("PATCH /admin/auth", () => {
		test("It should updated an user admin", async () => {
			const response = await request(domain)
										.patch('/admin/auth')
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

	//describe("PATCH /admin/auth/disabled", () => {
	//	test("It should disabled an user", async () => {
	//		const response = await request(domain)
	//									.patch('/admin/auth/disabled')
	//									.set('Authorization', 'Bearer ' + token);
	//		if (response.error) {
	//			console.log(response.error)
	//		}
	//		expect(response.statusCode).toBe(200);
	//	});

	//	afterAll(async () => {
	//		const response = await request(domain)
	//									.patch('/admin/auth/disabled')
	//									.set('Authorization', 'Bearer ' + token);
	//		if (response.error) {
	//			console.log(response.error)
	//		}
	//	})
	//});
	
	afterAll(async () => {
		const response = await request(domain)
									.delete('/admin/auth')
									.set('Authorization', 'Bearer ' + token);
		if (response.error) {
			console.log(response.error)
		}
	});
});


