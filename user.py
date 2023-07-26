from flask import Blueprint,render_template,session,redirect,url_for

user_dp = Blueprint('user',__name__,url_prefix='/user')

# @user_dp.route('/list')
# def user_list():
#     user_list=[]
#     return render_template('user/user_list.html',user=user_list)

@user_dp.route('/user_info')
def user_info():
    if 'user'in session:
        return render_template('user/user_info.html')
    else:
        return redirect(url_for('index'))
    
