import re
import apiAI.chatgpt as apiGpt
import json

strNo = ["www", "@","http:"]
strYes = [""]
def detect_dieu(text):
    # Biểu thức chính quy để tìm "điều 27." mà không phân biệt chữ hoa và chữ thường
    pattern = r'điều\s+\d+\.'

    # Sử dụng hàm findall() để tìm tất cả các sự xuất hiện của biểu thức chính quy trong văn bản
    matches = re.findall(pattern, text, re.IGNORECASE)

    # Trả về danh sách các kết quả nếu có kết quả trả về true 
    if len(matches) > 0:
        return True
    else:
        return False
    
def split_sections(text):
    lines = text.splitlines()
    sections = []
    paragraph = []
    current_section = ""
    level_same = 0
    mo = 1

    for line in lines:
        # Kiểm tra xem dòng có bắt đầu bằng số và dấu chấm hay không
        if (re.match(r'^\s*(\d+|[IVXLCDMivxlcdmtpabcdefjh]+)\.', line) and all(no not in line for no in strNo)) or detect_dieu(line)  :
            # Nếu có, lưu phần trước đó vào danh sách phần
            if current_section:
                level_same = level_of_arr(current_section,sections)
                if level_same == 0:
                    str = current_section.strip()
                    sections.append({"paragraph":str , "level":level_same})
                else:
                    sections.append({"paragraph":current_section.strip(), "level":level_same})
            current_section = line
        else:
            # Nếu không, thêm dòng vào phần hiện tại
            # Kiểm tra xuống hàng hợp lệ

            current_line = line.strip()
            if current_line and ((current_line[0].islower()) or current_line[-1] == ' '):
                current_section += ' ' + line
            else:
                current_section += '\n' + line


    # Lưu phần cuối cùng vào danh sách phần
    if current_section:
        level_same = level_of_arr(current_section, sections)
        sections.append({"paragraph": current_section.strip(), "level": level_same})

    return sections

def is_same_level(num1, num2):
    num1 = num1.lstrip()
    num2 = num2.lstrip()
    if (num1.islower() and num2.islower()) or (not num1.islower() and not num2.islower()):
        # đều là số
        if num1.isdigit() and num2.isdigit():
            return True
        elif not num1.isdigit() and not num2.isdigit():
            return True
        else:
            return False
    else:
        return False

def level_of_arr(str, arr):
    i = 1
    if len(arr) != 0:
        if arr[-1]["level"] == 0:
            if is_same_level(str.split('.')[0], arr[-1]["paragraph"].split('.')[0]) and countDots(arr[-1]["paragraph"],' ') == countDots(str,' '):
                 return 0
            return 1
        t = countDots(arr[-i]["paragraph"],' ') == countDots(str,' ')
        r = is_same_level(str.split('.')[0], arr[-i]["paragraph"].split('.')[0])
        while i <= len(arr):
            if '.' in arr[-i]["paragraph"] and countDots(arr[-i]["paragraph"],' ') == countDots(str,' ') :
                if is_same_level(str.split('.')[0], arr[-i]["paragraph"].split('.')[0]):
                  return arr[-i]["level"]
            elif countDots(arr[-i]["paragraph"],' ') == countDots(str,' '):
                if is_same_level(str.split('.')[0], arr[-i]["paragraph"].split(' ')[0]):
                  return arr[-i]["level"]
            i += 1
        return arr[-1]["level"]+1
    return 0

# Đém các dấu chấm (char)= ' ' trong chuỗi
def countDots(str, char):
    # Tách các phần số bằng dấu chấm và loại bỏ các ký tự không phải số
    str = str.lstrip()
    numbers = [num for num in str.split(char)[0].split('.') if num != '']

    return len(numbers)

#Xóa bỏ Ký tự phân cấp đối với paragraph có level = 0 
def delete_char_start(str):
    if re.match(r'^\s*(\d+|[IVXLCDMivxlcdmtpabcdefjh]+)\.', str) and all(no not in str for no in strNo):
        result_str = str.split(' ',1 )
        if len(result_str) >= 2:
            return result_str[1]
        
    return str 
    

# Từng đoạn đến level 0 tiếp theo
def split_sections_zero(sections, arr):
    newSection = []
    leaderParagraphs = []
    sum = 0
    # level có cấp bậc thấp nhất
    min_level = 0;
    i = 0
  
        
    while i < len(sections) and (sections[i]["level"] != 0 or sum == 0):
        sum += len(sections[i]["paragraph"].split(' '))
        if min_level < sections[i]["level"]:
            min_level = sections[i]["level"]
        i += 1

    if sum > 300 and len(sections) > 1 :
#         Tách mảng ra thành dạng menu
        count_leader_paragraph = 0 
        for section in sections:
            #Xoa cac #*# truoc do
        
            if '\n' in section["paragraph"] and " #*# " in section["paragraph"]:
                t = section["paragraph"].split("\n")[:]
                section["paragraph"] = t[0].split(" #*# ")[0] +"\n"+ "\n".join(t[1:])            
            if section["level"] != min_level or min_level == 1:
                sectionCopy = section.copy()
                if count_leader_paragraph != 0: 
                    sectionCopy["paragraph"] = sectionCopy["paragraph"].split('\n')[0]
                else:
                    if '\n' in sectionCopy["paragraph"]:
                        t = sectionCopy["paragraph"].split('\n')[:]
                        sectionCopy["paragraph"] = delete_char_start(t[0]) + '&menu&'
                        y = {"level": sectionCopy["level"] + 1, "paragraph": "Nội dung : " +'\n'+ '\n'.join(t[1:])}
                        sections.insert( count_leader_paragraph + 1, y)
                    else:
                        sectionCopy["paragraph"] = delete_char_start(sectionCopy["paragraph"]) + '&menu&'
                    
                        
                    
                arr.append(sectionCopy)
                    
            count_leader_paragraph += 1 
                
        section_pre = {"level":sections[0]["level"], "paragraph":sections[0]["paragraph"]}

        for section in sections:
          
                        
            if section["level"] != 0 :
                if section_pre != "" :
                    if section_pre["level"] < section["level"]:
                        if '\n' in section_pre["paragraph"]:
                            t = section_pre["paragraph"].split('\n')[:]
            
                            leaderParagraphs.append(delete_char_start(t[0]))
                        else: 
                            leaderParagraphs.append(delete_char_start(section_pre["paragraph"][:]))
                    elif section_pre["level"] > section["level"]:
                        leaderParagraphs.pop()
                if '\n' in section["paragraph"]:
                    set_leader = section["paragraph"].split('\n')[:]
                    #Xóa bỏ Ký tự phân cấp đối với paragraph có level = 0 
                    set_leader2 = delete_char_start(set_leader[0])
                    tam = {"level":section["level"] - 1, "paragraph":set_leader2 + " #*# " + leaderParagraphs[-1] + '\n' + "\n".join(set_leader[1:]) }
                else:
                    #Xóa bỏ Ký tự phân cấp đối với paragraph có level = 0 
                    section["paragraph"] = delete_char_start(section["paragraph"])
                    tam = {"level":section["level"] - 1, "paragraph":section["paragraph"] + " #*# " + leaderParagraphs[-1] }
                newSection.append(tam)
                
            section_pre = {"level":section["level"], "paragraph":section["paragraph"]}
        
        return fineSection(newSection, arr)  
        

        
    else:
        count_leader_paragraph = 0 
        
        for section in sections:  
            sectionCopy = section.copy()
            if count_leader_paragraph == 0 and section["level"] == 0:
                if '\n' in sectionCopy["paragraph"]:
                    section["paragraph"] = delete_char_start(sectionCopy["paragraph"].split('\n')[0] )+ '\n' + sectionCopy["paragraph"].split('\n', 1)[1] 
                else:
                    section["paragraph"] = delete_char_start(sectionCopy["paragraph"] )
            arr.append(section)      
            count_leader_paragraph += 1 
        return  arr 


    
# Tạo ra menu và nội dung hoàn chỉnh
def fineSection(sections,arr):
    tampSection = []
    fineSection = []
    for section in sections:
        if(section["level"] == 0):
            for item in split_sections_zero(tampSection, arr ):
                fineSection.append(item)
            tampSection = []
        tampSection.append(section)
# Them lần cuối
    for item in split_sections_zero(tampSection, arr ):
        fineSection.append(item)
    return arr

#Chuyển đổi dữ liệu sang dạng json để chatbot có thể train 
def convert_data_to_json(sections):
    arr_intent = []
    tag = ""
    patterns = []
    responses = []
    response = ""
    leader_paragraph = ""
    count = 0 
    for section in sections:
        if section["level"] == 0: 
            
            if count != 0:
                responses.append(response)
                arr_intent.append({"tag": tag,"patterns": patterns, "responses": responses})
            patterns = []
            responses = []
            response = ""
            if '&menu&' in section["paragraph"]:
                #xóa ký tự '&menu&' vì đã nhận diện được đây là menu không cần giữ lại '&menu&'
                section["paragraph"] = section["paragraph"].replace('&menu&', "")
                leader_paragraph = "" 
            else:                
                leader_paragraph = section["paragraph"][:]
            if '\n' in section["paragraph"]:              
                split_section = section["paragraph"].split('\n')
                patterns.append(split_section[0])
                tag = tag_standardizationt(split_section[0])
            else:
                patterns.append(section["paragraph"])
                tag = tag_standardizationt(section["paragraph"])  
        else:  
            #kiểm tra đây có phải những phần tử của menu (&menu&)
            if leader_paragraph != "":
                if '\n' in section["paragraph"]:
                    set_leader = delete_char_start(section["paragraph"].split('\n')[0][:])
                    tam = set_leader
                    patterns.append(tam)
                else:
                    patterns.append(section["paragraph"])       
            
        if count != 0:
            response += '\n' + section["paragraph"]
        else:
            response += section["paragraph"]
        count += 1 
       
    #Them doan  cuoi 
    responses.append(response)
    arr_intent.append({"tag": tag,"patterns": patterns, "responses": responses})    
    return arr_intent
    
    
# Chuẩn hóa tag     
def tag_standardizationt(original_string):
    words = original_string.split()  # Tách các từ theo khoảng trắng
    lowercase_words = [word.lower() for word in words]  # Chuyển đổi thành chữ cái thường
    result_string = [word.capitalize() for word in lowercase_words]
    result_string = ''.join(result_string)  # Nối các từ lại thành một chuỗi
    
    return result_string

def write_fileJson(answers):
    tas = {"intents":answers}
    with open("data/secondData/jsonAdvice.json", "w", encoding="utf-8") as f_output:
        json.dump(tas, f_output, ensure_ascii=False, indent=2)
# Ví dụ sử dụng hàm với nội dung từ file dataInput.txt
def standardize_data(input_file, output_file):
    with open(input_file, 'r', encoding='utf-8') as f_input:
        with open(output_file, 'w', encoding='utf-8') as f_output:
            content = f_input.read()
            sections = split_sections(content)
            sections2 = fineSection(sections,[])
            sectionsJson = convert_data_to_json(sections2)
            # sau khi phan tách các section thì đưa cho chatgpt.py liệt kê câu hỏi
            #question = "tôi muốn tạo chatbot trả lời câu hỏi và với nội dung thế này, hãy liệt kê những câu hỏi thường được sử dụng liên quan đến trọng tâm của nội dung "
            # answers = apiGpt.answer_The_Questions(sections2, question)
            # tas = [{'tag': '8KhungThờiGianRaVàoLớp', 'patterns': [' Buổi học có bao nhiêu tiết?', ' Tiết học đầu tiên vào lúc mấy giờ?', ' Tiết học cuối cùng vào lúc mấy giờ?', ' Giờ giải lao kéo dài bao lâu?', ' Buổi sáng có tổng cộng bao nhiêu tiết học?', ' Buổi chiều có tổng cộng bao nhiêu tiết học?', ' Buổi tối có tổng cộng bao nhiêu tiết học?', ' Cuối buổi học vào lúc mấy giờ?'], 'responses': ['\n8. KHUNG THỜI GIAN RA – VÀO LỚP\nPHỤ LỤC 2\nKHUNG THỜI GIAN RA – VÀO LỚP\nBuổi học Tiết học Giờ bắt đầu Giờ kết thúc\nSáng\nTiết 1 7:00 7:50\nTiết 2 7:50 8:40\nGiải lao 8:40 8:55\nTiết 3 8:55 9:45\nTiết 4 9:45 10:35\nBố trí 4,5 tiết 11:00\nChiều\nTiết 1 13:00 13:50\nTiết 2 13:50 14:40\nGiải lao 14:40 14:55\nTiết 3 14:55 15:45\nTiết 4 15:45 16:35\nBố trí 4,5 tiết 17:00\nTối 5 Bố trí 3,0 tiết Từ 17:30 đến 20:00']}, {'tag': '9GiớiThiệuVềHệThốngThôngTinDànhChoSinhViên', 'patterns': [' Trang web chính của trường là gì?', ' Trang web đăng ký môn học trực tuyến là gì?', ' Làm thế nào để đăng ký môn học trực tuyến?', ' Trang web cung cấp dịch vụ sinh viên là gì?', ' Làm thế nào để sử dụng hệ thống dịch vụ sinh viên?', ' Nơi nào có thể truy cập vào thông tin học tập trực tuyến?', ' Làm sao để sử dụng hệ thống elearning?', ' Cách truy cập vào hệ thống email của sinh viên?', ' Trang web nào hỗ trợ học tập online?', ' Làm sao để đặt sách online?', ' Nơi nào giới thiệu thông tin về việc làm cho sinh viên?', ' Có trang web nào giới thiệu dịch vụ của phòng Công tác Sinh viên không?'], 'responses': ['\n9. GIỚI THIỆU VỀ HỆ THỐNG THÔNG TIN DÀNH CHO SINH VIÊN\nHệ thống thông tin Trường Đại học Mở Thành phố Hồ Chí Minh trên mạng\nInternet cung cấp cho sinh viên các dịch vụ sau:\nWebsite chính của trường tại địa chỉ: www.ou.edu.vn\nĐây là nơi cung cấp các thông tin giới thiệu về trường. Giới thiệu thông tin về các khoa, phòng ban trực thuộc về chức năng, nhiệm vụ, đội ngũ quản lý, giảng viên và nhân viên, chương trình đào tạo,... Ngoài ra website còn cung cấp các thông báo cho sinh viên, tin tức về các hoạt động của trường.\n20 Sổ tay sinh viên 2022\nHệ thống đăng ký môn học trực tuyến tại địa chỉ: https://tienichsv.ou.edu.vn\n(hoặc từ trang web vào mục: “Đăng ký môn học trực tuyến”)\nĐây là nơi sinh viên có thể đăng ký môn học thông qua mạng internet.\nVào đầu mỗi học kỳ, từng sinh viên có thể chủ động chọn đăng ký các môn học phù hợp với mình, vào các nhóm (lớp) được mở trong thời gian thích hợp cho mỗi cá nhân. Để sử dụng hệ thống này, mỗi sinh viên dùng mã số sinh viên như tên đăng nhập. Sinh viên thường xuyên vào http://ou.edu.vn/qldt để xem kế hoạch và quy định đào tạo hằng năm của trường.\nHệ thống dịch vụ sinh viên tại địa chỉ: http://sis.ou.edu.vn\n(hoặc từ trang web vào mục: “Hệ thống thông tin sinh viên”)\nĐây là nơi cung cấp các tiện ích về lịch học, lịch thi, điểm thi, kiểm tra khóa mã, ... của sinh viên và các dịch vụ online khác. Để sử dụng hệ thống này sinh viên cần nhập mã số sinh viên, và mật khẩu.\nSinh viên chính quy: http://learn.ou.edu.vn (cổng thông tin học tập trực tuyến)\nSinh viên hệ từ xa, vừa làm, vừa học: http://lms.oude.edu.vn\nĐây là nơi sinh viên có thể truy cập và tham gia vào các lớp học của khoa để lấy tài liệu, bài giảng, xem thông báo của giáo viên, tham gia các diễn đàn...\nĐể sử dụng hệ thống elearning, sinh viên sử dụng tên đăng nhập là mã số sinh viên, mật khẩu là mật khẩu của hệ thống đăng ký môn học, tên hiển thị là tên sinh viên.\nHệ thống email sử dụng hạ tầng Google Apps tại địa chỉ: https://mail.google.com/mail\nSinh viên khi vào trường sẽ được cấp một tài khoản email trên hạ tầng\nGoogle apps là: Mã số sinh viên + Tên + @ou.edu.vn\nNhà trường sẽ gửi các thông tin, thông báo cho sinh viên thông qua hộp thư này.\nHệ thống Hỗ trợ học tập online: http://lms.ou.edu.vn\nHệ thống hỗ trợ đặt sách online tại địa chỉ: http://thuquan.ou.edu.vn\nĐây là nơi sinh viên có thể truy cập để đặt sách online của Nhà trường.\nTrang web giới thiệu thông tin về các tựa sách của tất cả các khoa, ban nhằm phục vụ cho việc học tập của sinh viên.\nCổng thông tin việc làm: http://vieclam.ou.edu.vn\nHệ thống dịch vụ của phòng Công tác Sinh viên: http://ou.edu.vn sau đó vào mục [sinh viên]\n Sổ tay sinh viên 2022 21']}]
            write_fileJson(sectionsJson)
            print("hoan thanh")


# Gọi hàm để chuẩn hóa dữ liệu từ dataInput.txt đến dataOutput.txt
standardize_data("data/firstData/inputAdvice.txt", "dataOutput.txt")