import numpy as np
import random
import json
import subprocess
import torch
import sys
import torch.nn as nn
import os 
from torch.utils.data import Dataset, DataLoader

from nltk_utils import bag_of_words, tokenize, stem, initVncorenlp, deactivate, create_and_activate_virtualenv,run_code_in_virtualenv
from model import NeuralNet


print(sys.prefix)
# Create and activate virtual environment
#create_and_activate_virtualenv("venv_init")
activate_script = create_and_activate_virtualenv("venv_init")
#---
ignore_words = [':', '?', '.', '!']
# Code to run in the virtual environment
code_to_run = '''



subprocess.run(["pip", "install", "py-vncorenlp"])
import py_vncorenlp
import numpy as np
import random
import json
import subprocess
import torch
import sys
import torch.nn as nn

from torch.utils.data import Dataset, DataLoader

from nltk_utils import bag_of_words, tokenize, stem, initVncorenlp, deactivate, create_and_activate_virtualenv,run_code_in_virtualenv
from model import NeuralNet

print("import py-vncorenlp")
with open('data/output.json', 'r', encoding='utf-8') as f:
    intents = json.load(f)
model1 = initVncorenlp()
print("init model1")
all_words = []
tags = []
xy = []
print(sys.prefix)

# loop through each sentence in our intents patterns
for intent in intents['intents']:
    tag = intent['tag']
    # add to tag list
    tags.append(tag)
    for pattern in intent['patterns']:
        # tokenize each word in the sentence
        w = tokenize(pattern, model1)
        w = [{"wordForm": stem(item["wordForm"]), "posTag": item["posTag"]} for item in w]        
        # add to our words list
        all_words.extend(w)
        # add to xy pair
        xy.append((w, tag))


# Khai báo biến ignore_words và gán giá trị
ignore_words = [":","?", ".", "!"]
print(ignore_words)
print(all_words)

# stem and lower each word
all_words_tam = []
#all_words = [item for item in all_words if item["wordForm"] not in ignore_words]
for item in all_words:
    if item["wordForm"] not in ignore_words:
        all_words_tam.append(item)
        print(item)

all_words = all_words_tam
# remove duplicates and sort
unique_words = []
for word in all_words:
    if word not in unique_words:
        unique_words.append(word)
all_words = unique_words
all_words = sorted(all_words, key=lambda x: x["wordForm"])

tags = sorted(set(tags))

data = {
    "all_words": all_words,
    "tags": tags,
    "xy": xy
}
print("All Words:", all_words)
print("Tags:", tags)
print("XY:", xy)


# Use an absolute path to save the data file
data_file_path = os.path.join(os.path.dirname(__file__), 'data', 'data.json')
with open(data_file_path, 'w', encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False)

'''

# Run the code in the virtual environment
run_code_in_virtualenv(code_to_run, activate_script)


# Use an absolute path to load the data file
data_file_path = os.path.join(os.path.dirname(__file__), 'data', 'data.json')
with open(data_file_path, 'r', encoding="utf-8") as f:
    data = json.load(f)

all_words = data["all_words"]
tags = data["tags"]
xy = data["xy"]

# Now you can use all_words, tags, and xy in your current environment
print("All Words:", all_words)
print("Tags:", tags)
print("XY:", xy)
#---


#print(sys.prefix)
## Install required packages for the first code block
#subprocess.run(["pip", "install", "py-vncorenlp"])    
## Run the first code block
#import py_vncorenlp    
#print("import py-vncorenlp")
#model1 = initVncorenlp()
#print("init model1")
#all_words = []
#tags = []
#xy = []
#print(sys.prefix)
## loop through each sentence in our intents patterns
#for intent in intents['intents']:
    #tag = intent['tag']
    ## add to tag list
    #tags.append(tag)
    #for pattern in intent['patterns']:
        ## tokenize each word in the sentence
        #w = tokenize(pattern, model1)
        #w = [{"wordForm": stem(item["wordForm"]), "posTag": item["posTag"]} for item in w]        
        ## add to our words list
        #all_words.extend(w)
        ## add to xy pair
        #xy.append((w, tag))
  
##close the virtual environment  
#deactivate()

# create training data
X_train = []
y_train = []
for (pattern_sentence, tag) in xy:
    # X: bag of words for each pattern_sentence
    bag = bag_of_words(pattern_sentence, all_words)
    X_train.append(bag)
    # y: PyTorch CrossEntropyLoss needs only class labels, not one-hot
    label = tags.index(tag)
    y_train.append(label)

X_train = np.array(X_train)
y_train = np.array(y_train)

# Hyper-parameters 
num_epochs = 1000
batch_size = 8
learning_rate = 0.001
input_size = len(X_train[0])
hidden_size = 32 
output_size = len(tags)
print(input_size, output_size)

class ChatDataset(Dataset):

    def __init__(self):
        self.n_samples = len(X_train)
        self.x_data = X_train
        self.y_data = y_train

    # support indexing such that dataset[i] can be used to get i-th sample
    def __getitem__(self, index):
        return self.x_data[index], self.y_data[index]

    # we can call len(dataset) to return the size
    def __len__(self):
        return self.n_samples

dataset = ChatDataset()
train_loader = DataLoader(dataset=dataset,
                          batch_size=batch_size,
                          shuffle=True,
                          num_workers=0)

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

model = NeuralNet(input_size, hidden_size, output_size).to(device)

# Loss and optimizer
criterion = nn.CrossEntropyLoss()
optimizer = torch.optim.Adam(model.parameters(), lr=learning_rate)

# Train the model
for epoch in range(num_epochs):
    for (words, labels) in train_loader:
        words = words.to(device)
        labels = labels.to(dtype=torch.long).to(device)
        
        # Forward pass
        outputs = model(words)
        # if y would be one-hot, we must apply
        # labels = torch.max(labels, 1)[1]
        loss = criterion(outputs, labels)
        
        # Backward and optimize
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()
        
    if (epoch+1) % 100 == 0:
        print (f'Epoch [{epoch+1}/{num_epochs}], Loss: {loss.item():.4f}')


print(f'final loss: {loss.item():.4f}')

data = {
"model_state": model.state_dict(),
"input_size": input_size,
"hidden_size": hidden_size,
"output_size": output_size,
"all_words": all_words,
"tags": tags
}
print(data)
current_file_dir = os.path.dirname(os.path.abspath(__file__))
FILE = os.path.join(current_file_dir, 'data/dataTrain.pth')

torch.save(data, FILE)

print(f'training complete. file saved to {FILE}')
