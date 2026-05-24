from flask import Flask
app=Flask(__name__)

@app.route('/')
def homee():
    return "Hello World!<br>Welcome to Flask"

if __name__=="__main__":
    app.run()
