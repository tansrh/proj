import random
import json

import torch

from model import NeuralNet
from nltk_utils import bag_of_words, tokenize

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

with open('intents.json', 'r') as json_data:
    intents = json.load(json_data)

FILE = "data.pth"
data = torch.load(FILE)

input_size = data["input_size"]
hidden_size = data["hidden_size"]
output_size = data["output_size"]
all_words = data['all_words']
tags = data['tags']
model_state = data["model_state"]

model = NeuralNet(input_size, hidden_size, output_size).to(device)
model.load_state_dict(model_state)
model.eval()

bot_name = "HealthBot"
'''
print("Let's chat! (type 'quit' to exit)")
while True:
    # sentence = "do you use credit cards?"
    sentence = input("Input: ")
    if sentence == "quit":
        break
'''
def get_response(sentence):


    sentence = tokenize(sentence)
    X = bag_of_words(sentence, all_words)
    X = X.reshape(1, X.shape[0])
    X = torch.from_numpy(X).to(device)

    output = model(X)
    _, predicted = torch.max(output, dim=1)

    tag = tags[predicted.item()]

    probs = torch.softmax(output, dim=1)
    prob = probs[0][predicted.item()]
    x="\n"
    print("\n")
    print(f"{bot_name}:")
    
    rec=""
    for intent in intents['intents']:

        if tag == intent["tag"]:
            if(tag not in ("greeting", "goodbye", "thanks", "funny")):
                    print("\n")
                    x=x+"\n" 
                    print(f"Possible case of {tag}")
                    x=x+("Possible case of "+ tag)
                    print("Accuracy: ", prob.item())
                    

            
            lst = intent['treatments']
            random_values = random.sample(lst, 5)
            print("Treatments:")
            x=x+"\n"
            x=x+("Treatments:")
            x=x+"\n"
            
            
            for i in random_values:
                print(i)
                x=x+(i)
                x=x+"\n"
                rec=rec+(i)

            print("\n")
            x=x+"\n"
            lst=intent['medications']
           
            
            random_values = random.sample(lst, 5)

            print("Medications:")
            x=x+("Medications:")
            x=x+"\n"
            for i in random_values:

                print(i)
                x=x+(i)
                x=x+"\n"

            print("\n")
            x=x+("\n")
            return [x,rec]
            break
    return x

