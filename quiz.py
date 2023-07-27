from flask import Blueprint,render_template,session,url_for,redirect,request
import db,random
from datetime import timedelta

quiz_dp = Blueprint('quiz',__name__,url_prefix='/quiz')

@quiz_dp.route('/quiz_register_form', methods=['GET'])
def quiz_register():
    if 'user'in session:
        user=session.get('user')
        if user[8]:
            type_list=db.select_all_type()
            return render_template('quiz/quiz_register.html',type_list=type_list)
        else:
            return render_template('quiz_top.html')
    else:
        return redirect(url_for('index'))
    
@quiz_dp.route('/quiz_type_register_form', methods=['GET'])
def quiz_type_register_form():
    if 'user'in session:
        user=session.get('user')
        if user[8]:
            return render_template('quiz/quiz_type_register.html')
        else:
            return render_template('quiz_top.html')
    else:
        return redirect(url_for('index'))
    

@quiz_dp.route('/quiz_type_register_exe',methods=['POST'])
def quiz_type_register_exe():
    if 'user'in session:
        user=session.get('user')
        if user[8]:
            quiz_type=request.form.get('quiz_type')

            if quiz_type == '':
                error ='クイズタイプが未入力です。'
                return render_template('quiz/quiz_register.html',error=error)
            count = db.insert_quiz_type(quiz_type)
            if count == 1:
                msg ='クイズタイプ登録が完了しました。'
                return redirect(url_for('index'))
            else:
                error='クイズタイプ登録に失敗しました。'
                return render_template('quiz/quiz_type_register.html',error=error)
        else:
            return render_template('quiz_top.html')
    else:
        return redirect(url_for('index'))
    
        
@quiz_dp.route('/quiz_register_exe',methods=['POST'])
def quiz_register_exe():
    type_list=db.select_all_type()
    if 'user'in session:
        user=session.get('user')
        if user[8]:
            quiz_title=request.form.get('quiz_title')
            quiz_type=request.form.get('quiz_type')
            quiz_content=request.form.get('quiz_content')
            quiz_answer=request.form.get('quiz_answer')
            quiz_choice1=request.form.get('quiz_choice1')
            quiz_choice2=request.form.get('quiz_choice2')
            quiz_choice3=request.form.get('quiz_choice3')
            quiz_choice4=request.form.get('quiz_choice4')
            if quiz_title == '':
                error ='クイズタイトルが未入力です。'
                return render_template('quiz/quiz_register.html',error=error,type_list=type_list)
            if quiz_type == '':
                error ='クイズタイプが未入力です。'
                return render_template('quiz/quiz_register.html',error=error,type_list=type_list)
            if quiz_content == '':
                error ='クイズの内容が未入力です。'
                return render_template('quiz/quiz_register.html',error=error,type_list=type_list)
            if quiz_answer == '':
                error ='答えが未入力です。'
                return render_template('quiz/quiz_register.html',error=error,type_list=type_list)
            
            if  quiz_choice1== '':
                error ='選択肢１が未入力です。'
                return render_template('quiz/quiz_register.html',error=error,type_list=type_list)
            if  quiz_choice2== '':
                error ='選択肢２が未入力です。'
                return render_template('quiz/quiz_register.html',error=error,type_list=type_list)

            if  quiz_choice3== '':
                error ='選択肢３が未入力です。'
                return render_template('quiz/quiz_register.html',error=error,type_list=type_list)

            if  quiz_choice4== '':
                error ='選択肢４が未入力です。'
                return render_template('quiz/quiz_register.html',error=error,type_list=type_list)
            
            count = db.insert_quiz(quiz_title,quiz_type,quiz_content,quiz_answer,quiz_choice1,quiz_choice2,quiz_choice3,quiz_choice4)
            if count == 1:
                msg ='クイズ登録が完了しました。'
                return render_template('quiz/quiz_register_result.html')
            else:
                error='クイズ登録に失敗しました。'
                return render_template('quiz/quiz_register.html',error=error,type_list=type_list)
        else:
            return render_template('quiz_top.html')
    else:
        return redirect(url_for('index'))
    
    

@quiz_dp.route('/list')
def quiz_list():
    if 'user'in session:
        quiz_list = db.select_all_quiz()
        print(quiz_list)
        return render_template('quiz/quiz_list.html', quizs=quiz_list)
    else:
        return redirect(url_for('index'))
    

@quiz_dp.route('/info')
def quiz_info():
    if 'user'in session:
        number = request.args.get('id')
        print(number)
        id=int(number)
        quiz_one= db.select_quiz_info(id)
        user=session.get('user')
        if user[8]:
            return render_template('quiz/quiz_info_root.html', quiz=quiz_one)
        else:
            return render_template('quiz/quiz_info.html', quiz=quiz_one)
    else:
        return redirect(url_for('index'))
    

@quiz_dp.route('/quiz_select_exe',methods=['POST'])
def quiz_select_exe():
    if 'user'in session:
        select_quiz=request.form.get('select_quiz')
        if select_quiz == '':
            error =''
            return render_template('quiz/quiz_register.html',error=error)
        quiz_list = db.select_quiz(select_quiz)
        if quiz_list != None:
            msg ='クイズ登録が完了しました。'
            return render_template('quiz/quiz_list.html', quizs=quiz_list)
        else:
            error='クイズ検索に失敗しました。'
            return render_template('quiz/quiz_list.html',error=error)
    else:
        return redirect(url_for('index'))
    

@quiz_dp.route('/quiz/quiz_delete')
def quiz_delete():
    if 'user'in session:
        user=session.get('user')
        if user[8]:
            quiz_number =request.args.get('quiz_number')
            quiz_title = request.args.get('quiz_title')
            quiz_type = request.args.get('quiz_type')
            quiz_content=request.args.get('quiz_content')
            quiz_answer=request.args.get('quiz_answer')
            quiz_choice1=request.args.get('quiz_choice1')
            quiz_choice2=request.args.get('quiz_choice2')
            quiz_choice3=request.args.get('quiz_choice3')
            quiz_choice4=request.args.get('quiz_choice4')
            return render_template('quiz/quiz_delete.html',quiz_number= quiz_number,quiz_title =quiz_title,quiz_type = quiz_type,quiz_content =quiz_content,quiz_answer = quiz_answer,quiz_choice1=quiz_choice1,quiz_choice2=quiz_choice2,quiz_choice3 =quiz_choice3,quiz_choice4=quiz_choice4 )
        else:
            return render_template('quiz_top.html')
    else:
        return redirect(url_for('index'))
    

@quiz_dp.route('/quiz/quiz_delete_exe')
def quiz_delete_exe():
    if 'user'in session:
        user=session.get('user')
        if user[8]:
            number=int(request.args.get('number'))
            count= db.delete_quiz(number)
            if count == 1:
                msg ='クイズ削除が完了しました。'
                return render_template('quiz/quiz_delete_result.html')
            else:
                error='クイズ削除に失敗しました。'
                return render_template('quiz/quiz_delete.html',error=error)
        else:
            return render_template('quiz_top.html')
    else:
        return redirect(url_for('index'))
    

@quiz_dp.route('/quiz/quiz_update')
def quiz_update():
    type_list=db.select_all_type()
    if 'user'in session:
        user=session.get('user')
        if user[8]:
            quiz_number =request.args.get('quiz_number')
            quiz_title = request.args.get('quiz_title')
            quiz_type = request.args.get('quiz_type')
            quiz_content=request.args.get('quiz_content')
            quiz_answer=request.args.get('quiz_answer')
            quiz_choice1=request.args.get('quiz_choice1')
            quiz_choice2=request.args.get('quiz_choice2')
            quiz_choice3=request.args.get('quiz_choice3')
            quiz_choice4=request.args.get('quiz_choice4')
            return render_template('quiz/quiz_update.html',quiz_number= quiz_number,quiz_title =quiz_title,quiz_type = quiz_type,quiz_content =quiz_content,quiz_answer = quiz_answer,quiz_choice1=quiz_choice1,quiz_choice2=quiz_choice2,quiz_choice3 =quiz_choice3,quiz_choice4=quiz_choice4 ,type_list=type_list)
        else:
            return render_template('quiz_top.html')
    else:
        return redirect(url_for('index'))

@quiz_dp.route('/quiz/quiz_update_exe',methods=['POST'])
def quiz_update_exe():
    type_list=db.select_all_type()
    if 'user'in session:
        user=session.get('user')
        if user[8]:
            quiz_number =int(request.args.get('quiz_number'))
            quiz_title = request.form.get('quiz_title')
            quiz_type = request.form.get('quiz_type')
            quiz_content=request.form.get('quiz_content')
            quiz_answer=int(request.form.get('quiz_answer'))
            quiz_choice1=request.form.get('quiz_choice1')
            quiz_choice2=request.form.get('quiz_choice2')
            quiz_choice3=request.form.get('quiz_choice3')
            quiz_choice4=request.form.get('quiz_choice4')
            count= db.update_quiz(quiz_number,quiz_title,quiz_type,quiz_content,quiz_answer,quiz_choice1,quiz_choice2,quiz_choice3,quiz_choice4,type_list=type_list)
            
            if quiz_title == '':
                error ='クイズタイトルが未入力です。'
                return render_template('quiz/quiz_update.html',error=error,quiz_number= quiz_number,quiz_title =quiz_title,quiz_type = quiz_type,quiz_content =quiz_content,quiz_answer = quiz_answer,quiz_choice1=quiz_choice1,quiz_choice2=quiz_choice2,quiz_choice3 =quiz_choice3,quiz_choice4=quiz_choice4,type_list=type_list)
            if quiz_type == '':
                error ='クイズタイプが未入力です。'
                return render_template('quiz/quiz_update.html',error=error,quiz_number= quiz_number,quiz_title =quiz_title,quiz_type = quiz_type,quiz_content =quiz_content,quiz_answer = quiz_answer,quiz_choice1=quiz_choice1,quiz_choice2=quiz_choice2,quiz_choice3 =quiz_choice3,quiz_choice4=quiz_choice4,type_list=type_list)
            if quiz_content == '':
                error ='クイズの内容が未入力です。'
                return render_template('quiz/quiz_update.html',error=error,quiz_number= quiz_number,quiz_title =quiz_title,quiz_type = quiz_type,quiz_content =quiz_content,quiz_answer = quiz_answer,quiz_choice1=quiz_choice1,quiz_choice2=quiz_choice2,quiz_choice3 =quiz_choice3,quiz_choice4=quiz_choice4,type_list=type_list)
            if quiz_answer == '':
                error ='答えが未入力です。'
                return render_template('quiz/quiz_update.html',error=error,quiz_number= quiz_number,quiz_title =quiz_title,quiz_type = quiz_type,quiz_content =quiz_content,quiz_answer = quiz_answer,quiz_choice1=quiz_choice1,quiz_choice2=quiz_choice2,quiz_choice3 =quiz_choice3,quiz_choice4=quiz_choice4,type_list=type_list)
            
            if  quiz_choice1== '':
                error ='選択肢１が未入力です。'
                return render_template('quiz/quiz_update.html',error=error,quiz_number= quiz_number,quiz_title =quiz_title,quiz_type = quiz_type,quiz_content =quiz_content,quiz_answer = quiz_answer,quiz_choice1=quiz_choice1,quiz_choice2=quiz_choice2,quiz_choice3 =quiz_choice3,quiz_choice4=quiz_choice4,type_list=type_list)
            if  quiz_choice2== '':
                error ='選択肢２が未入力です。'
                return render_template('quiz/quiz_update.html',error=error,quiz_number= quiz_number,quiz_title =quiz_title,quiz_type = quiz_type,quiz_content =quiz_content,quiz_answer = quiz_answer,quiz_choice1=quiz_choice1,quiz_choice2=quiz_choice2,quiz_choice3 =quiz_choice3,quiz_choice4=quiz_choice4,type_list=type_list)

            if  quiz_choice3== '':
                error ='選択肢３が未入力です。'
                return render_template('quiz/quiz_update.html',error=error,quiz_number= quiz_number,quiz_title =quiz_title,quiz_type = quiz_type,quiz_content =quiz_content,quiz_answer = quiz_answer,quiz_choice1=quiz_choice1,quiz_choice2=quiz_choice2,quiz_choice3 =quiz_choice3,quiz_choice4=quiz_choice4,type_list=type_list)

            if  quiz_choice4== '':
                error ='選択肢４が未入力です。'
                return render_template('quiz/quiz_update.html',error=error,quiz_number= quiz_number,quiz_title =quiz_title,quiz_type = quiz_type,quiz_content =quiz_content,quiz_answer = quiz_answer,quiz_choice1=quiz_choice1,quiz_choice2=quiz_choice2,quiz_choice3 =quiz_choice3,quiz_choice4=quiz_choice4)
            count= db.update_quiz(quiz_number,quiz_title,quiz_type,quiz_content,quiz_answer,quiz_choice1,quiz_choice2,quiz_choice3,quiz_choice4,type_list=type_list)
            if count == 1:
                msg ='クイズ編集が完了しました。'
                return render_template('quiz/quiz_update_result.html')
            else:
                error='クイズ編集に失敗しました。'
                return render_template('quiz/quiz_update.html',error=error,quiz_number= quiz_number,quiz_title =quiz_title,quiz_type = quiz_type,quiz_content =quiz_content,quiz_answer = quiz_answer,quiz_choice1=quiz_choice1,quiz_choice2=quiz_choice2,quiz_choice3 =quiz_choice3,quiz_choice4=quiz_choice4,type_list=type_list)
        else:
            return render_template('quiz_top.html')
    else:
        return redirect(url_for('index'))
    
