import os, psycopg2, string, random,hashlib,datetime

def get_connection():
    url = os.environ['DATABASE_URL']
    connection = psycopg2.connect(url)
    return connection

def get_salt():
    charset = string.ascii_letters + string.digits
    salt = ''.join(random.choices(charset, k=30))
    return salt

#DBに登録処理
def insert_user(user_name,age,gender,email, password):
    dt_now = datetime.datetime.now()
    sql = "INSERT INTO python_quiz_user VALUES(default, %s, %s,%s,%s,%s,%s,%s,default)"
    salt=get_salt()
    hashed_password=get_hash(password,salt)
    
    # 例外処理
    try :
        connection = get_connection()
        cursor = connection.cursor()
        
        cursor.execute(sql, (user_name,gender,age,email,salt,hashed_password,dt_now))
        
        count = cursor.rowcount
        connection.commit()
    except psycopg2.DatabaseError :
        count = 0
    finally :
        cursor.close()
        connection.close()
        
    return count
#パスワードとソルトを使ってハッシュ化（ストレッチング）
def get_hash(password,salt):
    b_pw=bytes(password,"utf-8")
    b_salt=bytes(salt,"utf-8")
    hashed_password=hashlib.pbkdf2_hmac("sha256",b_pw,b_salt,1000).hex()
    return hashed_password

def login(mail, password):
    sql='SELECT * FROM python_quiz_user WHERE mail = %s'
    flg=None
    try:
        connection=get_connection()
        cursor=connection.cursor()
        cursor.execute(sql, (mail,))
        user=cursor.fetchone()
        print(user)
        if user!=None:
        # SQLの結果からソルトを取得
            salt=user[5]
        # DBから取得したソルト + 入力したパスワード からハッシュ値を取得
            hashed_password=get_hash(password, salt)
        # 生成したハッシュ値とDBから取得したハッシュ値を比較する
            if hashed_password==user[6]:
                flg=user
    except psycopg2.DatabaseError :
        flg=None
    finally:
        cursor.close()
        connection.close()
    return flg

def select_all_quiz():
    connection = get_connection()
    cursor = connection.cursor()
    sql = "SELECT * FROM python_quiz"
    
    cursor.execute(sql)
    rows=  cursor.fetchall()
    
    cursor.close()
    connection.close()
    return rows

def select_all_type():
    connection = get_connection()
    cursor = connection.cursor()
    sql = "SELECT * FROM python_quiz_type"
    
    cursor.execute(sql)
    rows=  cursor.fetchall()
    
    cursor.close()
    connection.close()
    return rows

def select_quiz(quiz_title):
    connection = get_connection()
    cursor = connection.cursor()
    sql = "SELECT * FROM python_quiz WHERE quiz_title LIKE  %s"
    
    cursor.execute(sql,('%'+quiz_title+'%',))
    rows=  cursor.fetchall()
    
    cursor.close()
    connection.close()
    return rows

def select_quiz_info(number):
    id = int(number)
    connection = get_connection()
    cursor = connection.cursor()
    sql = "SELECT * FROM python_quiz WHERE quiz_number = %s"
    
    cursor.execute(sql,(id,))
    rows=  cursor.fetchall()
    
    cursor.close()
    connection.close()
    return rows


def insert_quiz_type(quiz_type):
    sql = "INSERT INTO python_quiz_type VALUES(default,%s)"
    
    # 例外処理
    try :
        connection = get_connection()
        cursor = connection.cursor()
        
        cursor.execute(sql, (quiz_type,))
        
        count = cursor.rowcount
        connection.commit()
    except psycopg2.DatabaseError :
        count = 0
    finally :
        cursor.close()
        connection.close()
        
    return count

#DBに登録クイズ登録
def insert_quiz(quiz_tile,quiz_type,quiz_content,quiz_answer,quiz_choice1,quiz_choice2,quiz_choice3,quiz_choice4):
    sql = "INSERT INTO python_quiz VALUES(default,%s,%s,%s,%s,%s,%s,%s,%s)"
    
    # 例外処理
    try :
        connection = get_connection()
        cursor = connection.cursor()
        
        cursor.execute(sql, (quiz_tile,quiz_type,quiz_content,quiz_answer,quiz_choice1,quiz_choice2,quiz_choice3,quiz_choice4))
        
        count = cursor.rowcount
        connection.commit()
    except psycopg2.DatabaseError :
        count = 0
    finally :
        cursor.close()
        connection.close()
        
    return count

def delete_quiz(id):
    sql = "DELETE FROM  python_quiz WHERE quiz_number = %s"
    
    # 例外処理
    try :
        connection = get_connection()
        cursor = connection.cursor()
        
        cursor.execute(sql, (id,))
        
        count = cursor.rowcount
        connection.commit()
    except psycopg2.DatabaseError :
        count = 0
    finally :
        cursor.close()
        connection.close()
        
    return count

def update_quiz(quiz_number,quiz_title,quiz_type,quiz_content,quiz_answer,quiz_choice1,quiz_choice2,quiz_choice3,quiz_choice4):
    sql = "UPDATE python_quiz SET quiz_title = %s ,quiz_type = %s,quiz_content = %s ,quiz_answer = %s ,choice1 = %s ,choice2 = %s ,choice3 = %s ,choice4 = %s WHERE quiz_number = %s"
    # 例外処理
    try :
        connection = get_connection()
        cursor = connection.cursor()
        
        cursor.execute(sql, (quiz_title,quiz_type,quiz_content,quiz_answer,quiz_choice1,quiz_choice2,quiz_choice3,quiz_choice4,quiz_number,))
        
        count = cursor.rowcount
        connection.commit()
    except psycopg2.DatabaseError :
        count = 0
    finally :
        cursor.close()
        connection.close()
        
    return count
