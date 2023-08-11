import openai
import re
import time
# Thiết lập API key của bạn
# api_key = "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"
import openai
openai.api_key = "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"
# %%
messages = [
    {"role": "system", "content": "You are a kind helpful assistant."},
]
# %%

def normalize_text(text):
    # Loại bỏ các dấu câu
    text = re.sub(r'[^\w\s]', '', text)

    # Tách thành các từ
    words = text.split()

    # Chuyển đổi mỗi từ thành viết thường và viết hoa chữ cái đầu tiên
    normalized_words = [word.capitalize() for word in words]

    # Ghép lại các từ thành câu và trả về kết quả
    return ''.join(normalized_words)

def answer_The_Questions(questions, title):
    i = 0
    new_Question = ""
    answers = []
    answer = {}
    tag1 = ""
    tag2 = ""
    lenQuestion = len(questions)
    # answers = [{"tag": "greeting",
    #       "patterns": [
    #         "Xin chào",
    #         "Chào bạn",
    #         "Chào",
    #         "Hi"
    #       ],
    #       "responses": [
    #         "Xin chào! Tôi có thể giúp gì cho bạn?",
    #         "Chào bạn! Cần tôi giúp gì?",
    #         "Hello! Bạn cần hỗ trợ gì?"
    #       ]
    #     }]
    tag1 = normalize_text(questions[i]["paragraph"].split('\n')[0])
    while i < len(questions) :
        if (i != 0 and questions[i]["level"] == 0) or i == len(questions):
            if questions[i]["level"] == 0 and i != len(questions):
                tag2 = normalize_text(questions[i]["paragraph"].split('\n')[0])
            message = title + ' ' + new_Question
            try:
                # Nếu chữ quá nhiều thì lấy 15 chữ đầu tiên
                if len(message.split()) > 200:
                    message = message[:500]
                print(message)
                if message:
                    messages.append(
                        {"role": "user", "content": message},
                    )
                    chat = openai.ChatCompletion.create(
                        model="gpt-3.5-turbo",
                        # model="text-davinci-003",
                        messages=messages

                    )
                    # Kiểm tra nội dung của câu trả lời có chứa thông báo lỗi hay không

                reply = chat.choices[0].message.content
            except openai.OpenAIError as e:
                time.sleep(60)
                # Xử lý ngoại lệ (lỗi) được trả về từ API ChatGPT
                print(f"An error occurred: {e}")
                i+= 1
                continue
                # return answers
            arrLineReply = reply.split('\n')
            patterns = []
            for line in arrLineReply:
                if re.match(r'^\s*(\d+|[ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz-]+)\.', line):
                    count_number_pattern = re.compile(r'\d+\.')
                    # Sử dụng phương thức sub của re để thay thế các số đếm bằng chuỗi trống
                    question_without_count = re.sub(count_number_pattern, '', line)
                    patterns.append(question_without_count)
            answer["tag"] = tag1
            answer["patterns"] = patterns
            answer["responses"] = [new_Question]
            # Thêm bản sao
            answers.append(answer.copy())
            print(f"ChatGPT: {reply}" + "\n")

            print(f"{i}/{lenQuestion}")
            message = ""
            new_Question = '\n' + questions[i]["paragraph"]
            tag1 = tag2[:]
        else:
            new_Question += '\n' + questions[i]["paragraph"]
        i += 1
    return answers

def answer_question(question, title):
    message = title + ' ' + question
    reply = "Không có câu trả lời"
    try:
        if message:
            messages.append(
                {"role": "user", "content": message},
            )
            chat = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                # model="text-davinci-003",
                messages=messages

            )
            # Kiểm tra nội dung của câu trả lời có chứa thông báo lỗi hay không

        reply = chat.choices[0].message.content
    except openai.OpenAIError as e:
        time.sleep(60)
        # Xử lý ngoại lệ (lỗi) được trả về từ API ChatGPT
        print(f"An error occurred: {e}")    
        
    return reply

#while True:
    #message = input("User : ")
    #if message:
        #messages.append(
             #{"role": "user", "content": message},
         #)
        #chat = openai.ChatCompletion.create(
             #model="text-davinci-002", messages=messages
         #)

    #reply = chat.choices[0].message.content
    #print(f"ChatGPT: {reply}")
    #messages.append({"role": "assistant", "content": reply})
