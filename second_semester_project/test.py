from flask import Flask, render_template
import json

app = Flask(__name__)

# 변수
lists=["2021-08-06","2021-08-09","2021-08-08","2021-08-07", "2021-08-05"]
# print("add date")
# addlist = input()
# lists.append(addlist)

@app.route("/")
def home():
  return render_template("test.html")

@app.route("/str")
def str():
  return json.dumps(lists)



if __name__ == "__main__":
    try:
        app.run(host="0.0.0.0", debug=True)
    finally:
      print("hello")











# from flask import Flask, render_template

# app = Flask(__name__)

# # 변수
# str = "21.12.03"

# @app.route("/")
# def home():
#   return render_template(
#     'test.html',
#     string = str)



# if __name__ == "__main__":
#     try:
#         app.run(host="0.0.0.0")
#     finally:
#       print("hello")