from flask import Flask, render_template
app = Flask(__name__    )

@app.route('/', methods=['GET'])
def index():
    return render_template('base.html')

# @app.route('/login', methods=['POST', 'GET'])
# def login

@app.route('/login', methods=['POST','GET'])
def Login():
    if request.args.get('email'):

    return render_template('login.html')

if __name__ == '__main__':
    app.debug = True
    app.run()