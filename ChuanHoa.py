def standardize_data(input_file, output_file):
    try:
        with open(input_file, 'r', encoding='utf-8') as f_input:
            with open(output_file, 'w', encoding='utf-8') as f_output:
                for line in f_input:
                    current_line = line.strip()
                    if current_line and current_line[0].islower():
                        f_output.write(' ' + current_line)
                    else:
                        f_output.write('\n' + current_line)


        print("Chuẩn hóa dữ liệu thành công!")
    except FileNotFoundError:
        print(f"Không tìm thấy file {input_file}.")



# Gọi hàm để chuẩn hóa dữ liệu từ dataInput.txt đến dataOutput.txt
standardize_data("dataInput.txt", "dataOutput.txt")
