def process_data(input_string):
    # Tách các phần số bằng dấu chấm và loại bỏ các ký tự không phải số
    numbers = [int(num) for num in input_string.split('.') if num.isdigit()]

    return len(numbers), numbers


# Ví dụ sử dụng hàm:
input_data_1 = "1.3.14.5"
input_data_2 = "1.32.3."

count_1, numbers_1 = process_data(input_data_1)
count_2, numbers_2 = process_data(input_data_2)

print("Dữ liệu {} có {} số: {}".format(input_data_1, count_1, numbers_1))
print("Dữ liệu {} có {} số: {}".format(input_data_2, count_2, numbers_2))