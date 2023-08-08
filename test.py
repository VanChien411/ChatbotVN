import py_vncorenlp

# Automatically download VnCoreNLP components from the original repository
# and save them in some local machine folderr
py_vncorenlp.download_model(save_dir='C:/Users/phuth/AppData/Local/Programs/Python/Python311/Lib/site-packages/py_vncorenlp')

model = py_vncorenlp.VnCoreNLP(save_dir='C:/Users/phuth/AppData/Local/Programs/Python/Python311/Lib/site-packages/py_vncorenlp')
# Equivalent to: model = py_vncorenlp.VnCoreNLP(annotators=["wseg", "pos", "ner", "parse"], save_dir='/absolute/path/to/vncorenlp')

# Annotate a raw corpus
#model.annotate_file(input_file="/absolute/path/to/input/file", output_file="/absolute/path/to/output/file")

# Annotate a raw text
print(model.annotate_text("Ông Nguyễn Khắc Chúc  đang làm việc tại Đại học Quốc gia Hà Nội. Bà Lan, vợ ông Chúc, cũng làm việc tại đây."))
model.print_out(model.annotate_text("Ông A được A điểm. Chú ông vàng."))
model.print_out(model.annotate_text("Ông A là chú hàng xóng bên \nChú Ông vàng.\n Email: 2031@df"))