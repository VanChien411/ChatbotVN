import torch
from transformers import AutoModel, AutoTokenizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np


# Mảng các câu trong đoạn văn
paragraphs = [
    "6.3. Phòng Công tác Sinh viên và Truyền Thông Liên hệ: Phòng 003, 008 – 97 Võ Văn Tần, Phường Võ Thị Sáu, Quận 3 Điện thoại: (028) 39302146 – (028) 39300077",
    "Một câu khác trong đoạn văn Sinh viên Câu thứ ba trong đoạn vănCâu thứ ba trong đoạn văn",
    "Câu thứ ba trong đoạn văn"
]

# Câu hỏi nhập từ người dùng
question = "Liên hệ của Phòng Công tác Sinh viên và Truyền Thông?"


def init_phoBert():
    # Khởi tạo mô hình và tokenizer PhoBERT
    phobert = AutoModel.from_pretrained("vinai/phobert-base")
    tokenizer = AutoTokenizer.from_pretrained("vinai/phobert-base")
    return phobert, tokenizer

def get_response_phoBert(phobert, tokenizer, question, paragraphs):
    # Mã hóa đoạn văn và câu hỏi bằng PhoBERT
    paragraph_encoding = tokenizer(paragraphs, return_tensors='pt', padding=True, truncation=True)
    questions_encoding = tokenizer(question , return_tensors='pt', padding=True, truncation=True)
    
    # Tạo các vectơ biểu diễn cho đoạn văn và câu hỏi
    paragraph_embedding = phobert(**paragraph_encoding).last_hidden_state.mean(dim=1)
    question_embeddings = phobert(**questions_encoding).last_hidden_state.mean(dim=1)
    
    # Tính toán sự tương đồng bằng cosine similarity
    similarities = cosine_similarity(paragraph_embedding.detach().numpy(), question_embeddings.detach().numpy())
    
    # Lấy ra các chỉ số của các kết quả có độ tương đồng lớn hơn 0.4 
    threshold = 0.4 
    matching_indices = np.where(similarities > threshold)[0]
    
    return matching_indices
    
#phobert, tokenizer = init_phoBert()
#matching_indices = get_response_phoBert(tokenizer, question, paragraphs) 
#print(similarities)