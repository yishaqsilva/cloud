from flask import Flask, render_template, request
import tensorflow as t                                  
import requests
import os
import numpy as n
from datetime import datetime
app = Flask("cloud")

#define globals
global models
global root_date

root_date = datetime.strptime("10/05/2020", "%d/%m/%Y")
#loading the models
def prep_models():
    models = {
        "ember" : t.keras.models.load_model(r"C:\Users\USER\Desktop\code\PYTHON\projects\raine\models\ember.keras")
        #"raine" : t.keras.models.load_model("..\\models\\raine.keras"),
       # "eve"   : t.keras.models.load_model("..\\models\\eve.keras"),
      #  "mist": t.keras.models.load_model("..\\models\\mist.keras")
    }
    return models
    
def convert_date_to_offset(date_string):
    date_string = datetime.strptime(date_string, "%d/%m/%Y")
    return root_date.day - date_string.day

#code is shitty and inefficient. i am tired and exhausted and would rather mod minecraft whilst watching anime.
def get_testing_data():

    offset = 3424 #this is where the testing dataset begins

    fname = os.path.join("C:\\Users\\USER\\Documents\\datasets\\Our cleaned data2.csv")
    with open(fname) as f:
     data = f.read()

    lines = data.split("\n")
    header = lines[0].split(",")
    lines = lines[1:]

    target = n.zeros((len(lines),))
    raw_data = n.zeros((len(lines), len(header) - 1))
    for i, line in enumerate(lines):
        values = [float(x) for x in line.split(",")[1:]]
        target[i] = values[2]
        raw_data[i, :] = values[:]

    num_train_samples = int(0.5 * len(raw_data))
    num_val_samples = int(0.25 * len(raw_data))

    sampling_rate = 6
    sequence_length = 7
    delay = 7
    batch_size = 256

    test_dataset = t.keras.utils.timeseries_dataset_from_array(
    raw_data[:-delay],
    targets = target[delay:],
    sampling_rate=sampling_rate,
    sequence_length=sequence_length,
    shuffle=True,
    batch_size=batch_size,
    start_index=num_train_samples + num_val_samples)

    #print(num_train_samples + num_val_samples)
    return test_dataset #this is the remainder, equivalent to the number of testing samples
    
testing_data = get_testing_data()
print("!Successfully loaded testing dataset")

models = prep_models()
print("!Successfully loaded models")


def get_preceeding_records(date_string): #i find that nesting functions makes it additionally obvious where it belongs.its just nice structure

    #first we get the offset or index of the given date string
    offset = convert_date_to_offset(date_string)

    #model_input = n.array([sample for sample in testing_data[offset - 7 : offset]]) 
    for x,y in testing_data.take(offset):  # We only need the first batch (single record)
        model_input = x[offset]

    model_input = model_input[None, ...] #adding that silly None bit

    return model_input
    
    
@app.route("/", methods = ["GET"])
def index():
    return render_template("index.html")

@app.post("/weather")
def inference():
    date_string = request.form.get("date")
    model_name = "ember"
    input_data = get_preceeding_records(date_string);# get_input_for_time_series_inference(date) #pretty long name. just wanted it to be obvious.
    prediction = models[model_name](input_data, training=False)  # Ensure model is in inference mode
    #prediction = prediction.__getattr__("data")
    #intent = testing_data[convert_date_to_offset(date_string)]
    print(f"model predicted {prediction} against an actual value of intent")
    return f"{int(prediction[0][0])}"

#makes sense to have this before hand lol

print("cloud is active!")
app.run(port=9999, debug = True)
