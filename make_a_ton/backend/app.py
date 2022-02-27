from flask import(Flask,render_template,request,session,redirect,url_for,g)

class User:
    def __init__(self, id, username, password):
        self.id = id
        self.username = username
        self.password = password

    def __repr__(self):
        return f'<User: {self.username}>'

users = []
users.append(User(id=1, username='sree', password='yeet'))
users.append(User(id=2, username='sindhu', password='yeee'))
users.append(User(id=3, username='vaish', password='nani'))


app = Flask(__name__)
app.secret_key = 'someSecretKey_Yeeeet'

@app.before_request
def before_request():
    g.user = None
    if 'user_id' in session:
        user = [x for x in users if x.id == session['user_id']][0]
        g.user = user



@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        session.pop('user_id', None)

        username = request.form['Username']
        password = request.form['Password']

        user = [x for x in users if x.username == username][0]
        if user and user.password == password:
            session['user_id'] = user.id
            return redirect(url_for('profile'))
        return redirect(url_for('login'))

    return render_template('login.html')

@app.route('/profile')
def profile():
    if not g.user:
        return redirect(url_for('login'))
    return render_template('profile.html')


@app.route('/console_allocation',methods=['POST'])
def console_allocation():
    response = ""
    time = request.form['time']
    game = request.form['game']
    platform = request.form['platform']

    print(time)
    print(game)
    print(platform)
    if time == '3' :
        response = "Success"
        g.response = response
    return render_template('profile.html')

@app.route('/signup',methods=['POST'])
def signup():
    if request.form['password'] != request.form['pass_re']:
        return redirect(url_for('login'))
    print(request.form['password'])
    return redirect(url_for('login'))


if __name__ == "__main__":
    app.run(debug=True)