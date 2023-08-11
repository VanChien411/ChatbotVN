import nltk
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

# Các câu hỏi và câu trả lời mẫu
questions = [
    "Trung tâm Đào tạo Từ xa của NƠI SINH VIÊN LIÊN HỆ\nLiên hệ: Phòng 004 – 97 Võ Văn Tần, Phường Võ Thị Sáu, Quận 3",
    "Trung tâm Đào tạo trực tuyến của NƠI SINH VIÊN LIÊN HỆ\nLiên hệ: Phòng 505 - 97 Võ Văn Tần, Phường Võ Thị Sáu, Quận 3",
    "Yêu cầu đầu vào của môn Tin học là gì?",
    "Giảng viên của môn Văn là ai?"
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
    # Đường dẫn đến tệp chứa các stopwords riêng của bạn
    custom_stopwords_file = "data/stopwords_vn.txt"
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
    preprocessed_questions = [preprocess_text(question) for question in questions]
    # Tạo ma trận TF-IDF
  
    tfidf_matrix = vectorizer.fit_transform(preprocessed_questions)
    return tfidf_matrix

# Hàm trả lời câu hỏi
def get_response(vectorizer, user_input, tfidf_matrix, questions):
    preprocessed_input = preprocess_text(user_input)
    tfidf_input = vectorizer.transform([preprocessed_input])
    
    similarities = cosine_similarity(tfidf_input, tfidf_matrix)
  
    # Lấy ra các chỉ số của các kết quả có độ tương đồng lớn hơn 0.2
    threshold = 0.2
    threshold_indices = [index for index, similarity in enumerate(similarities[0]) if similarity > threshold]

    # Lấy các chỉ số của các giá trị tương đồng và sắp xếp chúng theo thứ tự giảm dần
    sorted_indices = np.argsort(similarities[0])[::-1]
    
    # Lấy ra 4 kết quả có độ tương đồng cao nhất
    top_k = 4  
    matching_indices = sorted_indices[:top_k]
    
    matching_indices = [item for item in matching_indices if item in threshold_indices]

    # Sử dụng các chỉ số để lấy các câu trả lời tương ứng
    #matching_responses = [questions[index] for index in matching_indices]    
    # Độ tương đồng cao nhất 
    #max_similarity = similarities.max()
    
    
    if len(matching_indices) != 0 :  # Ngưỡng tương đồng
        index = matching_indices[0]
        return questions[index]
    else:
        return "Xin lỗi, tôi không thể tìm thấy câu trả lời cho câu hỏi của bạn."

# Giao diện chatbot đơn giản
print("Chào mừng bạn đến với trường học ảo. Hãy đặt câu hỏi của bạn hoặc gõ 'exit' để thoát.")
vectorizer = init_TFidf_chatbot()
custom_stopwords = get_custom_stopwords_file()
#tạo ma trận cho mảng câu hỏi 
tfidf_matrix = create_TF_idf(vectorizer, questions)

while True:
    user_input = input("Bạn: ")
    if user_input.lower() == "exit":
        print("Chatbot: Tạm biệt!")
        break
    # đưa vào model đã khởi tạo, câu hỏi của người dùng, ma trận câu hỏi, và các câu hỏi để hiển thị câu trả lời 
    response = get_response(vectorizer, user_input,tfidf_matrix, questions)
    print("Chatbot:", response)
