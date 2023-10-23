import mysql.connector

# Thay thế các giá trị sau bằng thông tin của cơ sở dữ liệu MySQL của bạn
db_config = {
    "host": "localhost",
    "user": "root",
    "password": "",
    "database": "chatbotvn"
}

def create_connection():
    try:
        conn = mysql.connector.connect(**db_config)
        return conn
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None

# Hàm thêm phiên làm việc mới vào bảng `session`
def add_session(user_id, start_time):
    conn = create_connection()
    if conn:
        try:
            with conn.cursor() as cursor:
                add_session_query = "INSERT INTO session (user_id, start_time) VALUES (%s, %s)"
                session_data = (user_id, start_time)
                cursor.execute(add_session_query, session_data)
                conn.commit()
                return cursor.lastrowid  # Trả về ID của phiên làm việc vừa thêm
        except mysql.connector.Error as err:
            print(f"Error: {err}")
        finally:
            conn.close()

# Hàm thêm câu hỏi và câu trả lời vào bảng `question_answer`
def add_question_answer(session_id, question, answer):
    conn = create_connection()
    if conn:
        try:
            with conn.cursor() as cursor:
                add_qa_query = "INSERT INTO question_answer (session_id, question, answer) VALUES (%s, %s, %s)"
                qa_data = (session_id, question, answer)
                cursor.execute(add_qa_query, qa_data)
                conn.commit()
        except mysql.connector.Error as err:
            print(f"Error: {err}")
        finally:
            conn.close()

# Hàm truy vấn dữ liệu từ bảng `information`
def get_information():
    conn = create_connection()
    if conn:
        try:
            with conn.cursor() as cursor:
                select_info_query = "SELECT * FROM information"
                cursor.execute(select_info_query)
                result = cursor.fetchall()
                return result
        except mysql.connector.Error as err:
            # Throwing an exception so the caller can handle it
            raise Exception(f"Error in get_information: {err}")
        finally:
            conn.close()

# Hàm truy vấn dữ liệu từ bảng `session`
def get_session():
    conn = create_connection()
    if conn:
        try:
            with conn.cursor() as cursor:
                select_info_query = "SELECT * FROM session ORDER BY end_time DESC"
                cursor.execute(select_info_query)
                result = cursor.fetchall()
                return result
        except mysql.connector.Error as err:
            # Throwing an exception so the caller can handle it
            raise Exception(f"Error in get_information: {err}")
        finally:
            conn.close()

# Hàm truy vấn dữ liệu từ bảng `question_answer` dựa trên `session_id`
def get_qa_by_session(session_id):
    conn = create_connection()
    if conn:
        try:
            with conn.cursor() as cursor:
                select_info_query = "SELECT * FROM question_answer WHERE session_id = %s"
                cursor.execute(select_info_query, (session_id,))
                result = cursor.fetchall()
                return result
        except mysql.connector.Error as err:
            # Ném một ngoại lệ để cho người gọi xử lý
            raise Exception(f"Error in get_qa_by_session: {err}")
        finally:
            conn.close()

# Hàm truy vấn dữ liệu từ bảng `question_answer` dựa trên `session_id` mới nhất theo end_time 
def get_qa_by_session_first():
    session_first = get_session()[0]
    return get_qa_by_session(session_first[0])
    

def update_session_end_time(session_id, end_time):
    conn = create_connection()
    print(1) 
    if conn:
        try:
            with conn.cursor() as cursor:
                update_query = "UPDATE session SET end_time = %s WHERE session_id = %s"
                cursor.execute(update_query, (end_time, session_id))
                conn.commit()
        except Error as err:
            print(f"Error: {err}")
        finally:
            conn.close()
            
#session_data = get_qa_by_session(1)
#for info in session_data:
    #print(info)  
## Sử dụng hàm để lấy dữ liệu từ bảng `information`
#information_data = get_information()
#for info in information_data:
    #print(info)
## Gọi các hàm từ db_operations.py
#user_id = 1
#start_time = "2023-10-12 14:30:00"
#session_id = db_operations.add_session(user_id, start_time)

#db_operations.add_question_answer(session_id, "Câu hỏi 1", "Câu trả lời 1")
#db_operations.add_question_answer(session_id, "Câu hỏi 2", "Câu trả lời 2")
