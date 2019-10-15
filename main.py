from flask import Flask,render_template,url_for,request
import rfm_action as ac

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/action',methods=['GET','POST'])
def rfm_action():
    data = request.get_json()
    res = ac.rfm_do_action(data)
    return res

if __name__ == '__main__':
    app.debug = True
    app.run(
        host= '0.0.0.0'
    )
