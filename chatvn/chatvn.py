import random
import json
import torch
import py_vncorenlp
import numpy as np
import sys
sys.path.append('../') 
from model import NeuralNet


from nltk_utils import bag_of_words, tokenize, initVncorenlp, stem 

from natural_language_processing.tf_idf import init_TFidf_chatbot, get_custom_stopwords_file, create_TF_idf, get_response
from natural_language_processing.phoBert import init_phoBert,get_response_phoBert
from natural_language_processing.bard import get_synonyms_and_abbreviations,get_bard_answer
def get_response_torch(probs):
    # Lấy ra các nhãn có xác suất cao hơn một ngưỡng (ví dụ: 0.5)
    threshold = 0.3 
    selected_labels = [{"index": i, "similarity": prob.item()} for i, prob in enumerate(probs[0]) if prob.item() > threshold]
    # Lấy các chỉ số của các giá trị tương đồng và sắp xếp chúng theo thứ tự giảm dần
    sorted_indices = np.argsort([-prob.item() for prob in probs[0]])    
    # Lấy ra 4 kết quả có độ tương đồng cao nhất
    top_k = 4  
    matching_indices_index = sorted_indices[:top_k]
    
    matching_indices = []
    for item in matching_indices_index:
        for item2 in selected_labels:
            if item == item2["index"]:
                matching_indices.append({"tag": tags[item2["index"]], "similarity":item2["similarity"]})
                continue   
            
    #[{'tag': 'HànhChínhSinhViên', 'similarity': 0.38936707235389134}]
            
    # Mảng các câu trả lời tương đồng     
    return matching_indices


# So sánh câu trả lời
#arr[][] mỗi dòng là một mảng để so sánh 
def compare_answers(arr):
    sum = []
    isSame = False
    for i in arr:
        for j in i:
            for item in sum:
                if item["tag"] == j["tag"]:
                    item["similarity"] = (item["similarity"] + j["similarity"])/2
                    isSame = True
                    break
            if isSame == False:
                sum.append(j)
            else:
                isSame == False
   # Sắp xếp giảm dần
    sum = sorted( sum , key=lambda x: x["similarity"], reverse=True)
    
    return sum     

# Tiền sử lý câu hỏi sử lý các vấn đề xảy ra từ câu hỏi, dữ liệu vào là câu hỏi đã phân tách
def preprocess_question(second_sentence):
    #[
    #{vitri: 0, word: [Tổi chức y tế thế giới, Người ]},
    #{vitri:2, word: Cái gì}
    #] 
    arr_change_word = []
    
    # Khai báo biến ignore_words và gán giá trị
    count = 0 
    for item in second_sentence:
        # Kiểm tra có phải ký tự đặc biệt
        if item["posTag"] != 'CH':
            #Nếu là từ viết tắc
            #if item["posTag"] in [ 'Ny', 'Vy', 'Xy']:
                #arr_change_word.append({"index":count, "word":[item['wordForm']]})
           
            #Nếu từ viết sai chính tả 
          
            arr_change_word.append(item["wordForm"])
        count += 1
    
    
    #Nếu có từ đồng nghĩa va từ viết tắt  tra ve mang
    t = get_synonyms_and_abbreviations(" ".join(arr_change_word)) 
    #[
    #"giới thiệu hệ thống thông tin cho sinh viên",
    #"giới thiệu về hệ thống thông tin sinh viên",]
    return t 

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

with open('../data/secondData/jsonAdvice.json', 'r',encoding='utf-8') as json_data:
    intents = json.load(json_data)

FILE = "../data/trainData/Advice.pth"
data = torch.load(FILE)

input_size = data["input_size"]
hidden_size = data["hidden_size"]
output_size = data["output_size"]
all_words = data['all_words']
tags = data['tags']
model_state = data["model_state"]

model = NeuralNet(input_size, hidden_size, output_size).to(device)
model.load_state_dict(model_state)
model.eval()

# create tf-idf  ----

vectorizer = init_TFidf_chatbot()
custom_stopwords = get_custom_stopwords_file()
#tạo ma trận cho mảng câu hỏi 
tfidf_matrix, tfidf_tags = create_TF_idf(vectorizer, intents['intents'])   

#----
# create phoBert ---
phobert, tokenizer_phoBert = init_phoBert()
#---

bot_name = "Chatbot ou"

#create phoBert
model1 = initVncorenlp()
print("Let's chat! (type 'quit' to exit)")
def get_chatbot_response(sentence):
    # sentence = "do you use credit cards?"
    #sentence = input("You: ")
    user_of_quesion = sentence[:]
    if sentence == "quit":
        return ''
    
    # các câu hỏi tương tự
    arrQ = get_synonyms_and_abbreviations(sentence,3 )    
    print(arrQ)
    arrQ = []
    arrQ.append(sentence)
    # Vong lap tim cau tra loi phu hop nhat 
    max_similarity = 0.0  # Khởi tạo biến lưu trữ độ tương đồng lớn nhất
    best_tag = ""  # Biến lưu trữ tag tương ứng với độ tương đồng lớn nhất
    probs = None 
    for item in arrQ:
        sentence = tokenize(item, model1)
        print(sentence)
        
        X = bag_of_words(sentence, all_words)
        X = X.reshape(1, X.shape[0])
        X = torch.from_numpy(X).to(device)
        
        output = model(X)
        probs_tam = torch.softmax(output, dim=1)
        max_similarity_tam = torch.max(probs_tam)  # Lấy xác suất lớn nhất từ probs_tam
        
        if max_similarity_tam.item() > max_similarity:
            max_similarity = max_similarity_tam.item()
            _, predicted = torch.max(output, dim=1)
            best_tag = tags[predicted.item()]
            probs = probs_tam
        
        print(max_similarity_tam.item())
        print(f'Best Tag: {best_tag}')

        
    #-------
    #_, predicted = torch.max(output, dim=1)
    
    #tagMax = tags[predicted.item()]    
    #print(predicted.item())
    #print(f'TagMax : {tagMax}')
    #-------

    response_torch = get_response_torch(probs)
    
    response_tfidf = get_response(vectorizer, user_of_quesion,tfidf_matrix, tfidf_tags)
    
    compare_responses = []
    compare_responses.append(response_torch)
    compare_responses.append(response_tfidf)
    
    # Danh sách các câu trả lời phù hợp 
    compare_responses = compare_answers(compare_responses)
    count_break = 0  
    for item in compare_responses:
        for intent in intents['intents']:
            if item["tag"] == intent["tag"]:        
               
                
                # Sử lý tìm ra nội dung chính phù hợp với câu hỏi 
                paragraphs = random.choice(intent['responses']).split("\n")[:]
                matching_indices = get_response_phoBert(phobert, tokenizer_phoBert, user_of_quesion, paragraphs) 
                merged_paragraph = "\n".join([paragraphs[value] for value in matching_indices])
                print(f"{bot_name}:Đây là nội dung chính được sửa lý: \n {merged_paragraph}")
                #chatbot trả lời theo tag 
                print(f"\n Đây là nội dung gốc:\n {random.choice(intent['responses'])}")    
                if item["similarity"] < 0.3:
                    return get_bard_answer(user_of_quesion)
                return f"{random.choice(intent['responses'])}"
                # Xuất ra kết quả tốt nhất phần còn lại sẽ sử lý sau 
                count_break += 1 
                return ''
        else:
            print(f"{bot_name}: I do not understand...")
        if count_break != 1:
            return ''
    
    
#print(get_chatbot_response("Văn phòng các khoa"))