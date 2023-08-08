from nltk_utils import initVncorenlp, tokenize

model = initVncorenlp()
data = "Chào tôi là người lập trình bạn. Bạn có nhận thức được không.\n Tôi có thể làm gì giúp bạn."
arr = tokenize(data, model)
print(arr)