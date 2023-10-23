from bardapi import Bard
import os 
os.environ["_BARD_API_KEY"] = "cQh9MiwI3L1hbB6gsOWWFbzKUNmoyR65if7wP_1_vyoJ_mkKzxOlVpgjIjG6BiB-PvGx2Q."

"""
enter: tôi cần bạn liệt kê các từ đồng nghĩa và từ viết tắc của "công nghệ thông tin" vào mảng wordSum. Tuyệt đối không nói gì thêm, không cần giải thích hay chỉ cách làm
"""
word = """tôi cần bạn liệt kê các từ đồng nghĩa và từ viết tắc của "GIỚI THIỆU VỀ HỆ THỐNG TT DÀNH CHO SV" vào mảng wordSum. Tuyệt đối không nói gì thêm, không cần giải thích hay chỉ cách làm, không viết code """

# Từ đồng nghĩa và từ viết tắt
def get_synonyms_and_abbreviations(key, max_retries=3):
    word = f"""tôi cần bạn liệt kê các từ đồng nghĩa và từ viết tắc của "{key}" vào mảng wordSum. Tuyệt đối không nói gì thêm, không cần giải thích hay chỉ cách làm, không viết code. Phải có dạng wordSum = [], và phải có ít nhất một nội dung đầy đủ"""
    
    arrResult = []
    isWordSum = False
    retries = 0
    
    while retries < max_retries:
        result = Bard().get_answer(str(word))["content"]
        arrR = result.split()
        
        pre = ''
        for w in arrR:
            if isWordSum == True:
                arrResult.append(w)
                if w.count(']') > 0:
                    a = " ".join(arrResult)
                    if arrResult == None:
                        arrResult = []
                        isWordSum = False
                    
            if w.count("=") > 0 and pre.count("wordSum") > 0:
                isWordSum = True        
            pre = w
        
        if not arrResult:
            pre = ''
            for w in arrR:
                if isWordSum == True:
                    arrResult.append(w)
                    if w.count(']') > 0:
                        a = " ".join(arrResult)
                        if arrResult == None:
                            arrResult = []
                            isWordSum = False
                        else:
                            return a
                if (w.count("=") > 0 and pre.count("wordSum") > 0) or  pre.count("Kết quả") > 0:
                    isWordSum = True        
                pre = w            
        # Kiểm tra nếu kết quả là rỗng, thử lại
        if not arrResult:
            retries += 1
        else:
            t = " ".join(arrResult)
            c = 0 
            tam = ""
            arr = []
            for w in t:
               
               
                if w.count('"') > 0 or w.count("'") >0:
                    c += 1     
                    continue
                if c % 2 != 0:
                    tam += w
                else:
                    if tam != "":
                        arr.append(tam)
                    tam = ""
            print(arr)
            return arr
    
    return "Không có kết quả"


def get_bard_answer(question):
    result = Bard().get_answer(str(question))["content"]

    if result:
        return result
    else:
        return None
    
#y = get_bard_answer("Bạn biết gì về công nghệ thông tin ")
#print(y)
#t = get_synonyms_and_abbreviations("HT thogn tin ",3 )
    
#print(t)
