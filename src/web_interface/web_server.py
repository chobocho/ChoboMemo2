from flask import Flask, request

from web_interface.dbmanager import DBManager

app = Flask(__name__)

dbm = DBManager('minim.db')
dbData = dbm.load()
print(len(dbData))

class MinimWebServer:
    def __init__(self):
        ...

    @staticmethod
    @app.route('/')
    def index():
        print(">> ", request.method)
        print(">> ", request.headers)
        ret = ""
        count = 1000
        for _, item in dbData.items():
            if count == 0:
                break
            count -= 1
            ret += f"{item['id']}<br>"
        return f"?<h6>{ret}</h6>"

    @staticmethod
    @app.route('/user/<name>')
    def user(name):
        print(">>> ", request.headers)
        return '<h1>Hello, %s!</h1>' % name

    @staticmethod
    @app.after_request
    def after_request(response):
        print(">>>> ", response.headers)
        return response


if __name__ == '__main__':
    app.run(debug=True)
