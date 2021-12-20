from flask import Flask

# flask 객체 생성
app = Flask(__name__)

# 0.0.0.0:5000/


@app.route("/")
def hello():
  return '''
    <p>Hello, Flask!!</p>
    <a href="/first">Go First</a>
    <a href="/second">Go Second</a>
  '''

@app.route("/first")
def first():
  return '''
    <p>First Page</p>
    <a href="/">Go Home</a>
  '''

@app.route("/second")
def second():
  return '''
    <p>Second Page</p>
    <a href="/">Go Home</a>
  '''

# 터미널에서 직접 실행시킨 경우
if __name__ == "__main__":
  app.run(host="0.0.0.0")