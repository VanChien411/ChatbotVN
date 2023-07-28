import re

def split_sections(text):
    lines = text.splitlines()
    sections = []
    paragraph = []
    current_section = ""
    level_same = 0
    mo = 1
    for line in lines:
        # Kiểm tra xem dòng có bắt đầu bằng số và dấu chấm hay không
        if re.match(r'^\s*(\d+|[ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz]+)\.', line):
            # Nếu có, lưu phần trước đó vào danh sách phần
            if current_section:
                level_same = level_of_arr(current_section,sections)
                sections.append({"paragraph":current_section.strip(), "level":level_same})
            current_section = line
        else:
            # Nếu không, thêm dòng vào phần hiện tại
            # Kiểm tra xuống hàng hợp lệ

            current_line = line.strip()
            if current_line and (current_line[0].islower()):
                current_section += ' ' + line
            else:
                current_section += '\n' + line


    # Lưu phần cuối cùng vào danh sách phần
    if current_section:
        level_same = level_of_arr(current_section, sections)
        sections.append({"paragraph": current_section.strip(), "level": level_same})

    return sections

def is_same_level(num1, num2):

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
    numbers = [num for num in str.split(char)[0].split('.') if num != '']

    return len(numbers)

# Từng đoạn đến level 0 tiếp theo
def split_sections_zero(sections, arr):
    newSection = []
    sum = 0
    # level có cấp bậc thấp nhất
    min_level = 0;
    i = 0
    while i < len(sections) and (sections[i]["level"] != 0 or sum == 0):
        sum += len(sections[i]["paragraph"].split(' '))
        if min_level < sections[i]["level"]:
            min_level = sections[i]["level"]
        i += 1

    if sum > 300 and len(sections) > 1:
#         Tách mảng ra thành dạng menu
        for section in sections:
            if section["level"] != min_level:
                arr.append(section)
        for section in sections:
            if section["level"] != 0:
                tam = {"level":section["level"] - 1, "paragraph":section["paragraph"]}
                newSection.append(tam)

        return split_sections_zero(newSection, arr)
    else:
        for section in sections:
            arr.append(section)
        return arr

# Tạo ra menu và nội dung hoàn chỉnh
def fineSection(sections):
    tampSection = []
    fineSection = []
    for section in sections:
        if(section["level"] == 0):
            for item in split_sections_zero(tampSection, []):
              fineSection.append(item)
            tampSection = []
        tampSection.append(section)
# Them lần cuối
    for item in split_sections_zero(tampSection, []):
        fineSection.append(item)
    return fineSection

# Ví dụ sử dụng hàm với nội dung từ file dataInput.txt
def standardize_data(input_file, output_file):
    with open(input_file, 'r', encoding='utf-8') as f_input:
        with open(output_file, 'w', encoding='utf-8') as f_output:
            content = f_input.read()
            sections = split_sections(content)
            sections2 = fineSection(sections)
            print("hoan thanh")
            for section in sections:
                f_output.write(section["paragraph"] + '\n')

# Gọi hàm để chuẩn hóa dữ liệu từ dataInput.txt đến dataOutput.txt
standardize_data("dataInput.txt", "dataOutput.txt")