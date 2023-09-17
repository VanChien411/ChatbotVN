input_file = "data/firstData/inputAdvice.txt"
output_file = "data/firstData/test.txt"

with open(input_file, 'r', encoding='utf-8') as f_input:
    with open(output_file, 'w', encoding='utf-8') as f_output:
        for line in f_input:
            # Kiểm tra nếu dòng bắt đầu bằng a), b), c),...
            if line.strip().startswith(('a)', 'b)', 'c)', 'd)', 'e)','đ)','f)','g)','h)')):
                for prefix in ('a)', 'b)', 'c)', 'd)', 'e)','đ)','f)','g)','h)'):
                    if line.lstrip().startswith(prefix):
                        line = '+' + line.lstrip(prefix)

            # Ghi dòng đã chỉnh sửa vào tệp output
            f_output.write(line)
