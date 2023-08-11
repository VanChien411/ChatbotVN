import random
import json
import torch
import py_vncorenlp
import numpy as np
from model import NeuralNet
from apiAI.chatgpt import answer_question

from nltk_utils import bag_of_words, tokenize, initVncorenlp, stem 

from natural_language_processing.tf_idf import init_TFidf_chatbot, get_custom_stopwords_file, create_TF_idf, get_response

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
    

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

with open('data/output.json', 'r',encoding='utf-8') as json_data:
    intents = json.load(json_data)

FILE = "data/dataTrain.pth"
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

bot_name = "Chatbot ou"

#create phoBert
model1 = initVncorenlp()
print("Let's chat! (type 'quit' to exit)")
while True:
    # sentence = "do you use credit cards?"
    sentence = input("You: ")
    user_of_quesion = sentence[:]
    if sentence == "quit":
        break
        
    sentence = tokenize(sentence,model1)
    sentence = [{"wordForm": stem(item["wordForm"]), "posTag": item["posTag"]} for item in sentence]        
    print(sentence)
   
    X = bag_of_words(sentence, all_words)
    X = X.reshape(1, X.shape[0])
    X = torch.from_numpy(X).to(device)

    output = model(X)
    probs = torch.softmax(output, dim=1)
    
    #-------
    _, predicted = torch.max(output, dim=1)
    
    tagMax = tags[predicted.item()]    
    print(predicted.item())
    print(f'TagMax : {tagMax}')
    #-------

    response_torch = get_response_torch(probs)
    
    response_tfidf = get_response(vectorizer, user_of_quesion,tfidf_matrix, tfidf_tags)
    
    compare_responses = []
    compare_responses.append(response_torch)
    compare_responses.append(response_tfidf)
    
    # Danh sách các câu trả lời phù hợp 
    compare_responses = compare_answers(compare_responses)
        
    for item in compare_responses:
        for intent in intents['intents']:
            if item["tag"] == intent["tag"]:        
                #chatbot trả lời theo tag 
                print(f"{bot_name}: {random.choice(intent['responses'])}")
                # Xuất ra kết quả tốt nhất phần còn lại sẽ sử lý sau 
                break
        else:
            print(f"{bot_name}: I do not understand...")
    
    
    