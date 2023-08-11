import nltk
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import os 

# Các câu hỏi và câu trả lời mẫu
questions = [
    {
      "tag": "HànhChínhSinhViên",
      "patterns": [
        "HÀNH CHÍNH SINH VIÊN"
      ],
      "responses": [
        "HÀNH CHÍNH SINH VIÊN\nCác vấn đề liên quan đến xác nhận hạnh kiểm, tham gia hoạt động ngoại  khóa"
      ]
    },
    {
      "tag": "NơiSinhViênLiênHệ",
      "patterns": [
        "NƠI SINH VIÊN LIÊN HỆ"
      ],
      "responses": [
        "\nNƠI SINH VIÊN LIÊN HỆ\n6.1. Văn phòng các khoa\n6.2. Phòng Quản lý đào tạo\n6.4. Phòng Tài chính – Kế toán\n6.5. Trạm Y tế\n6.6. Phòng Khảo thí\n6.7. Thư viện\n6.8. Đoàn Thanh niên – Hội Sinh viên\n6.9. Trung tâm Quản lý hệ thống thông tin\n6.10. Phòng Thanh tra – Pháp chế\n6.11. Khoa khoa học cơ bản\n6.12. Phòng Hợp tác & Quản lý khoa học\n6.13. Trung tâm Đào tạo ngắn hạn và Ngoại ngữ - Tin học (Center for\n6.14. Trung tâm Đào tạo Từ xa\n6.15. Trung tâm Đào tạo trực tuyến\n6.16. Trung tâm học liệu"
      ]
    }
]

answers = [
    "Học phí của môn học là $100.",
    "Lịch học của môn Toán là vào thứ Hai và thứ Tư.",
    "Yêu cầu đầu vào của môn Tin học là kiến thức cơ bản về lập trình.",
    "Giảng viên của môn Văn là thầy Nguyễn Văn A."
]

def init_TFidf_chatbot():
    # Tiền xử lý văn bản
    nltk.download('punkt')
    nltk.download('stopwords')  
    vectorizer = TfidfVectorizer()
    # Trả về dạng model để sử dụng 
    return vectorizer
    
def get_custom_stopwords_file():
   # Lấy đường dẫn đến thư mục của script hiện tại
    current_file_dir = os.path.dirname(os.path.abspath(__file__))

    # Lấy đường dẫn đến dự án hiện tại bằng cách thêm đường dẫn tương đối từ thư mục của script
    project_dir = os.path.join(current_file_dir, '..')  # '..' là đường dẫn tương đối để đi từ thư mục hiện tại lên một cấp

    # Đường dẫn đến tệp stopwords_vn.txt trong dự án hiện tại
    file_path = os.path.join(project_dir, 'data/stopwords_vn.txt')  
    # Đường dẫn đến tệp chứa các stopwords riêng của bạn
    custom_stopwords_file = file_path
    # Đọc tệp và tạo mảng stopwords
    stop_words = []
    with open(custom_stopwords_file, "r", encoding="utf-8") as file:
        for line in file:
            word = line.strip()  # Loại bỏ dấu xuống dòng và khoảng trắng
            if word:
                stop_words.append(word)    
    return stop_words


def preprocess_text(text):
    stop_words = get_custom_stopwords_file()
    words = nltk.word_tokenize(text.lower())
    words = [word for word in words if word.isalnum() and word not in stop_words]
    return ' '.join(words)

def create_TF_idf(vectorizer, questions):
    preprocessed_questions =[]
    tags = []
    for question in questions:
        for response in question["responses"]:
            preprocessed_questions.append(preprocess_text(response))
            tags.append(question["tag"])
        
    # Tạo ma trận TF-IDF
  
    tfidf_matrix = vectorizer.fit_transform(preprocessed_questions)
    return tfidf_matrix, tags

# Hàm trả lời câu hỏi
def get_response(vectorizer, user_input, tfidf_matrix, tags):
    preprocessed_input = preprocess_text(user_input)
    tfidf_input = vectorizer.transform([preprocessed_input])
    
    similarities = cosine_similarity(tfidf_input, tfidf_matrix)
  
    # Lấy ra các chỉ số của các kết quả có độ tương đồng lớn hơn 0.2
    threshold = 0.2
    threshold_indices = [{"index": index, "similarity": similarity} for index, similarity in enumerate(similarities[0]) if similarity > threshold]    
    # Lấy các chỉ số của các giá trị tương đồng và sắp xếp chúng theo thứ tự giảm dần
    sorted_indices = np.argsort(similarities[0])[::-1]
    
    # Lấy ra 4 kết quả có độ tương đồng cao nhất
    top_k = 4  
    matching_indices_index = sorted_indices[:top_k]
    
    matching_indices = []
    for item in matching_indices_index:
        for item2 in threshold_indices:
            if item == item2["index"]:
                matching_indices.append({"tag": tags[item2["index"]], "similarity":item2["similarity"]})
                continue

    # Sử dụng các chỉ số để lấy các câu trả lời tương ứng
    #matching_responses = [questions[index] for index in matching_indices]    
    # Độ tương đồng cao nhất 
    #max_similarity = similarities.max()
    
    #[{'tag': 'HànhChínhSinhViên', 'similarity': 0.38936707235389134}]
    
    # Mảng các câu trả lời tương đồng 
    return matching_indices
   

# Giao diện chatbot đơn giản
print("Chào mừng bạn đến với trường học ảo. Hãy đặt câu hỏi của bạn hoặc gõ 'exit' để thoát.")
#vectorizer = init_TFidf_chatbot()
#custom_stopwords = get_custom_stopwords_file()
##tạo ma trận cho mảng câu hỏi 
#tfidf_matrix, tags = create_TF_idf(vectorizer, questions)

#while True:
    #user_input = input("Bạn: ")
    #if user_input.lower() == "exit":
        #print("Chatbot: Tạm biệt!")
        #break
    ## đưa vào model đã khởi tạo, câu hỏi của người dùng, ma trận câu hỏi, và các câu hỏi để hiển thị câu trả lời 
    #response = get_response(vectorizer, user_input,tfidf_matrix, tags)
    #print("Chatbot:", response)
