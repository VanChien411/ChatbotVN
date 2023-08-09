import py_vncorenlp
import numpy as np
import nltk
from nltk.stem.porter import PorterStemmer
import os
import sys
import subprocess
stemmer = PorterStemmer()

def create_and_activate_virtualenv(venv_name):
    # Create virtual environment
    subprocess.run(["python", "-m", "venv", venv_name])
    
    # Activate virtual environment
    if os.name == "nt":
        activate_script = os.path.join(venv_name, "Scripts", "activate")
    else:
        activate_script = os.path.join(venv_name, "bin", "activate")
        
    return activate_script

def run_code_in_virtualenv(code, activate_script):
    # Activate the virtual environment
    subprocess.run([activate_script], shell=True)
    print(activate_script)
    print("run")
    print(sys.prefix)
    # Run the code
    exec(code)
    
    # Deactivate the virtual environment
    subprocess.run(["deactivate"], shell=True)
    print("close venv")

def initVncorenlp():
  
    current_file_dir = os.path.dirname(os.path.abspath(__file__))
    vncorenlp_dir = os.path.join(current_file_dir,'venv_init','py_vncorenlp')
    
    # Automatically download VnCoreNLP components from the original repository
    # and save them in some local machine folderr
    py_vncorenlp.download_model(save_dir=vncorenlp_dir)
    
    model1 = py_vncorenlp.VnCoreNLP(save_dir=vncorenlp_dir)
    # Equivalent to: model = py_vncorenlp.VnCoreNLP(annotators=["wseg", "pos", "ner", "parse"], save_dir='/absolute/path/to/vncorenlp')
    
    # Annotate a raw corpus
    #model.annotate_file(input_file="/absolute/path/to/input/file", output_file="/absolute/path/to/output/file")
    return model1 

def deactivate():
    # Deactivate the virtual environment
    subprocess.run(["deactivate"])  
    print("Close the virtual environment")

def tokenize(sentence,model):
    """
    Split sentence into array of words/tokens
    """
    doc = model.annotate_text(sentence)
    result_array = []
    model.print_out(doc)
    # Trích xuất wordForm và posTag từ dictionary và lưu vào mảngdoc
    for key in doc:
        for item in doc[key]:
            wordForm = item['wordForm']
            posTag = item['posTag']
            result_array.append({'wordForm': wordForm, 'posTag': posTag})
    
    return result_array

def stem(word):
    """
    Stemming = find the root form of the word
    """
    # Return the lowercase word as it is without stemming
    return stemmer.stem(word.lower())

def bag_of_words(tokenized_sentence, words):
    """
    Return bag of words array:
    1 for each known word that exists in the sentence, 0 otherwise
    """

    # Initialize bag with 0 for each word
    bag = np.zeros(len(words), dtype=np.float32)
    for idx, w in enumerate(words):
        if w in tokenized_sentence:
            bag[idx] = 1

    return bag
