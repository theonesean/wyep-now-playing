from flask import Flask, request
app = Flask(__name__)

@app.route('/oauth_cb')
def oauth_cb():
    tok = request.args.get('oauth_token')
    sec = request.args.get('oauth_verifier')
    print('Params:', tok, sec)
    return 'Params: ' + tok + '\n' + sec

@app.route('/')
def hello_world():
    return 'Hello, World!'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000)