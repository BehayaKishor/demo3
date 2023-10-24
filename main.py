
from fastapi import FastAPI
from pydantic import BaseModel
import pickle
import json
import uvicorn
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class model_input(BaseModel):

    N :float
    P :float
    k :float
    temperature :float
    humidity :float
    ph :float
    rainfall :float

crop_model = pickle.load(open('model.pkl', 'rb'))

@app.post('/crop_yeild_recommendation')
def crop_pred(input_parameters : model_input):

    input_data = input_parameters.json()
    input_dictionary = json.loads(input_data)

    N = input_dictionary['N']
    P = input_dictionary['P']
    k = input_dictionary['k']
    temperature = input_dictionary['temperature']
    humidity = input_dictionary['humidity']
    ph = input_dictionary['ph']
    rainfall = input_dictionary['rainfall']



    input_list = [N, P, k, temperature, humidity, ph, rainfall]

    prediction = crop_model.predict([input_list])
    crop_dict = {1: "Rice", 2: "Maize", 3: "Jute", 4: "Cotton", 5: "Coconut", 6: "Papaya", 7: "Orange",
                 8: "Apple", 9: "Muskmelon", 10: "Watermelon", 11: "Grapes", 12: "Mango", 13: "Banana",
                 14: "Pomegranate", 15: "Lentil", 16: "Blackgram", 17: "Mungbean", 18: "Mothbeans",
                 19: "Pigeonpeas", 20: "Kidneybeans", 21: "Chickpea", 22: "Coffee"}

    if prediction[0] in crop_dict:
        crop = crop_dict[prediction[0]]
        return crop
    else:
        return -1

