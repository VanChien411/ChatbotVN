original_string = "Mục lục sổ tay sinh viên"
words = original_string.split()  # Tách các từ theo khoảng trắng
lowercase_words = [word.lower() for word in words]  # Chuyển đổi thành chữ cái thường
result_string = [word.capitalize() for word in lowercase_words]
result_string = ''.join(result_string)  # Nối các từ lại thành một chuỗi


print(result_string)  # In kết quả: "Mucluc_sotay_sinhvien"
