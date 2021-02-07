const request = require('supertest');
const { admin } = require('./config');
const { login } = require('./utils');


const domain = "http://api:3000/api/v1";

jest.setTimeout(100000)

describe("AuthAdmin", () => {
	let token = null;
	

	describe("POST /auth", () => {
		test("It should create an user", async () => {
			const response = await request(domain)
										.post('/auth')
										.set('Authorization', 'Bearer ' + token)
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
										.set('Authorization', 'Bearer ' + token)
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
										.set('Authorization', 'Bearer ' + token)
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
										.set('Authorization', 'Bearer ' + token)
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
});


