from flask import Flask,render_template,request,redirect,url_for,session
from datetime import timedelta
import db ,string,random
import mail
from user import user_dp
from quiz import quiz_dp

app = Flask(__name__)
app.secret_key=''.join(random.choices(string.ascii_letters,k=256))

app.register_blueprint(quiz_dp)
app.register_blueprint(user_dp)

@app.route('/',methods=['GET'])
def index():
    msg=request.args.get('msg')
    
    if msg == None:
        #通常アクセス
        return render_template('index.html')
    else:
        #user_register.exeからredirectされた場合
        return render_template('index.html',msg=msg)
    
@app.route('/',methods=['POST'])
def login():
    # error='ログインに失敗しました。'
    # return render_template('index.html',error=error)
    mail=request.form.get('mail')
    password=request.form.get('password')
    print(mail)
    print(password)
    # ログイン判定
    user=db.login(mail, password)
    if user==None:
        error='メールアドレスまたはパスワードが違います。'
        return render_template('index.html', error=error)
    else:
        session['user']=user
        session.permanent=True
        app.permanent_session_lifetime = timedelta(days=5)
        return redirect(url_for('mypage'))
@app.route('/mypage', methods=['GET'])
def mypage():
    if 'user'in session:
        user=session.get('user')
        if user[8]:
            return render_template('root_top.html')
        else:
            return render_template('quiz_top.html')
    else:
        return redirect(url_for('index'))
    
@app.route('/user_register')
def user_register_form():
    return render_template('user_register.html')

@app.route('/user_register_exe',methods=['POST'])
def user_register_exe():
    user_name=request.form.get('username')
    age=request.form.get('age')
    gender=request.form.get('gender')
    email=request.form.get('email')
    password=request.form.get('password')
    
    if user_name == '':
        error ='ユーザ名が未入力です。'
        return render_template('user_register.html',error=error)
    
    if age == '':
        error ='年齢が未入力です。'
        return render_template('user_register.html',error=error)
    if gender == '':
        error ='性別が未入力です。'
        return render_template('user_register.html',error=error)
    if email == '':
        error ='メールアドレスが未入力です。'
        return render_template('user_register.html',error=error)
        
    if password == '':
        error ='パスワードが未入力です。'
        return render_template('user_register.html',error=error)
    
    count = db.insert_user(user_name,age,gender,email,password)
    if count == 1:
        msg ='登録が完了しました。'
        return redirect(url_for('index',msg = msg))
    else:
        error='登録に失敗しました。'
        return render_template('user_register.html',error=error)
    
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

@app.route('/quiz_respond',methods=['GET','POST'])
def quiz_respond():
    if 'user'in session:
        answerd=session.get('respond')
        if answerd==None :
            quiz_list =list(db.select_all_quiz())
            random.shuffle(quiz_list)
            session['quiz_list']=quiz_list
            session['respond']=0
            session['correct_answer']=0
            session.permanent=True
            app.permanent_session_lifetime = timedelta(days=5)
            return render_template('quiz/quiz_respond.html')
        else:
            answer =int(request.form.get('answer'))
            print(answer)
            quiz_list = session.get('quiz_list')
            correct = session.get('correct_answer')
            result =correct
            if  quiz_list[answerd][4]== answer :
                result = correct+1
                session['correct_answer']=correct+1
            session['respond']=answerd+1
            if answerd == 9 :
                user=session.get('user')
                to=user[4]
                subject='クイズリザルト'
                if correct >=8:
                    body=f'この度はクイズアプリをご利用いただき誠にありがとうございます。今回の回答結果は10問正解中{result}問正解しました。おめでとうございます。'
                else:
                    body=f'この度はクイズアプリをご利用いただき誠にありがとうございます。今回の回答結果は10問正解中{result}問正解しました。次は高得点を目指して頑張りましょう'
                mail.send_mail(to,subject,body)
                return render_template('quiz/quiz_result.html')
            else:
                return render_template('quiz/quiz_respond.html')
    else:
        return redirect(url_for('index'))
    

@app.route('/top')
def quiz_session_clear():
    session.pop('respond')
    session.pop('correct_answer')
    session.pop('quiz_list')
    return redirect(url_for('mypage'))
    
   
    
if __name__=='__main__':
    app.run(debug=True)
    