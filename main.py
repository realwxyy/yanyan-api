import os
from flask import Flask
app = Flask(__name__)
@app.route('/')
def hello_world():
    return '嫣嫣是个小笨蛋 接口调用成功！'
if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=80)