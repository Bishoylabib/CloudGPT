import google.generativeai as genai
from openai import OpenAI
from flask import Flask, render_template, request, jsonify
import os


genai.configure(api_key='XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX') #Gemini API
client = OpenAI(api_key="XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX") # OpenAi Whisper API

model = genai.GenerativeModel('gemini-pro')

#audio_file = open("audiofiles/sa7aba.m4a", "rb")
# transcript = client.audio.transcriptions.create(
#     model="whisper-1",
#     file=audio_file,
#     response_format="text",
#     language="en", 
#     # make the language default to the language of the audio file
# )

# print(transcript)
# with open("transcription.txt", "w", encoding="utf-8") as f:
#     f.write(transcript)

messages = []

app = Flask(__name__)


@app.route('/record_audio', methods=["POST"])
def record_audio():
    print("enter the audio page")
    audio_blob = request.files['audioBlob']
    filename = "audio_1.webm"  # Adjust the filename as needed
    filepath = os.path.join('audiofiles', filename)  # Adjust the path as needed

    audio_blob.save(filepath)
        
    # Open the file that was just saved
    audio_file = open("audiofiles/audio_1.webm", "rb") 
    transcript = client.audio.transcriptions.create(
    model="whisper-1",
    file=audio_file,
    response_format="text",
    language="en", 
    # make the language default to the language of the audio file
    )  
    print(transcript)
    with open("transcription.txt", "w", encoding="utf-8") as f:
        f.write(transcript)
    return transcript

# def get_Chat_response_voice(audio):
#     #giving the chatbot commands using speech
#     messages.append({
#         "role": "user",
#         "parts": [str(audio)]
#     })
    
#     response = model.generate_content(messages)
#     response_text = response.text
#     for i in range(response_text.count('**')):
#         if i%2==0:
#             response_text = response_text.replace('**', '<strong>',1)
#         else:
#             response_text = response_text.replace('**', '</strong>',1) 
    
#     if messages:
#         model_response = {
#             "role": "model",
#             "parts": [response_text]
#         }
#         messages.append(model_response)
#         print(f'{model_response["parts"][0]}') 
#         return f'{model_response["parts"][0]}'
#     else:
#         return "No messages available."



@app.route("/")
def index():
    print("enter the home page")
    return render_template('chat.html')


@app.route("/get", methods=["GET", "POST"])
def chat():
    print("enter the message page")
    msg = request.form["msg"]
    input = msg
    return get_Chat_response(input)


def get_Chat_response(text):
    messages.append({
        "role": "user",
        "parts": [str(text)]
    })
    
    response = model.generate_content(messages)
    response_text = response.text
    for i in range(response_text.count('**')):
        if i%2==0:
            response_text = response_text.replace('**', '<strong>',1)
        else:
            response_text = response_text.replace('**', '</strong>',1) 
    
    if messages:
        model_response = {
            "role": "model",
            "parts": [response_text]
        }
        messages.append(model_response)
        return f'{model_response["parts"][0]}'
    else:
        return "No messages available."


if __name__ == '__main__':
    app.run()