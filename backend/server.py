import tornado.ioloop
import tornado.web
import pymysql.cursors
import json

# Database configuration
# Database configuration
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '@JohnSandeep123',
    'db': 'myappdb',
    'charset': 'utf8mb4',
    'cursorclass': pymysql.cursors.DictCursor,
}


# Initialize the database connection
connection = pymysql.connect(**db_config)

class RegistrationHandler(tornado.web.RequestHandler):
    def post(self):
        data = json.loads(self.request.body)
        username = data.get('username')
        password = data.get('password')

        try:
            with connection.cursor() as cursor:
                sql = "INSERT INTO users (username, password) VALUES (%s, %s)"
                cursor.execute(sql, (username, password))
                connection.commit()
                response = {"message": "Registration successful"}
                self.write(response)
        except Exception as e:
            response = {"message": "Registration failed", "error": str(e)}
            self.set_status(400)
            self.write(response)

class LoginHandler(tornado.web.RequestHandler):
    def post(self):
        data = json.loads(self.request.body)
        username = data.get('username')
        password = data.get('password')

        try:
            with connection.cursor() as cursor:
                sql = "SELECT * FROM users WHERE username = %s AND password = %s"
                cursor.execute(sql, (username, password))
                user = cursor.fetchone()
                if user:
                    response = {"message": "Login successful"}
                    self.write(response)
                else:
                    response = {"message": "Invalid username or password"}
                    self.set_status(401)
                    self.write(response)
        except Exception as e:
            response = {"message": "Login failed", "error": str(e)}
            self.set_status(400)
            self.write(response)

def make_app():
    return tornado.web.Application([
        ("/api/register", RegistrationHandler),
        ("/api/login", LoginHandler),
    ])

if __name__ == "__main__":
    app = make_app()
    app.listen(8888)  # Change the port as needed
    print("Server is running on port 8888")
    tornado.ioloop.IOLoop.current().start()
