from flask import Blueprint,render_template,session,redirect,url_for
import db

user_dp = Blueprint('user',__name__,url_prefix='/user')


@user_dp.route('/user_info')
def user_info():
    if 'user'in session:
        return render_template('user/user_info.html')
    else:
        return redirect(url_for('index'))
    

@user_dp.route('/user_log')
def user_log():
    if 'user'in session:
        user=session.get('user')
        user_one_log=db.select_quiz_log_one(user[0])
        return render_template('user/user_log.html',user_one_log=user_one_log)
    else:
        return redirect(url_for('index'))
    
@user_dp.route('/user_rank')
def user_rank():
    if 'user'in session:
        user_rank=db.select_quiz_log()
        size=len(user_rank)
        return render_template('user/user_rank.html',user_rank=user_rank,size=size)
    else:
        return redirect(url_for('index'))
    