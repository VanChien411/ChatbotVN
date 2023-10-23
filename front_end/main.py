from flask import Flask, request, render_template, jsonify
from datetime import datetime

import sys

sys.path.append('../')  # Thêm thư mục chứa chatvn.py vào sys.path
import database.mySQL as mySQL
from chatvn.chatvn import get_chatbot_response

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def index():
    
    return render_template('index.html')

@app.route('/chat', methods=['GET', 'POST'])  # Chỉ xử lý yêu cầu POST
def chat():
    user_question = ""
    answer = "ok1"

    if request.method == 'POST':
        user_question = request.form['user_question']
        # Thực hiện xử lý câu hỏi và lấy câu trả lời từ hệ thống chatbot ở đây
    
        # Gọi hàm xử lý câu trả lời từ tệp chatvn.py
        chatvn = get_chatbot_response(user_question)
        
        print(chatvn)
        return jsonify(answer=chatvn) # Trả về kết quả dưới dạng JSON
    return render_template('index.html', user_question=user_question, answer=chatvn)

# Tuyến đường để cung cấp dữ liệu từ bảng `information` dưới dạng JSON
@app.route('/get_information')
def get_information_json():
    information_data = mySQL.get_information()

    return jsonify(information_data)

@app.route('/get_session')
def get_session_json():
    session_data = mySQL.get_session()
    return jsonify(session_data)

@app.route('/get_qa_by_session/')
def get_qa_by_session():
    qa_by_session_data = mySQL.get_qa_by_session_first()
    return jsonify(qa_by_session_data)

@app.route('/update_session_end_time/<session_id>', methods=['PUT'])
def update_session_end_time(session_id):
    # Lấy thời gian hiện tại
    current_time = datetime.now()

    # Format thời gian thành chuỗi có định dạng SQL DATETIME
    formatted_time = current_time.strftime("%Y-%m-%d %H:%M:%S")

    # Cập nhật end_time của phiên làm việc
    mySQL.update_session_end_time(session_id, formatted_time)
    print(2)
    return "Session end time updated"

if __name__ == '__main__':
    app.run()

