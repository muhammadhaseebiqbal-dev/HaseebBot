from flask import Flask, jsonify, render_template, request
import google.generativeai as genai
import re
import requests
from PIL import Image
from io import BytesIO
import base64
from better_profanity import profanity
from chunks.aiConfig import model
from chunks.chatHistory import createChatStorage,conversation_histories

app = Flask(__name__)


# Default Route i.e; Main page rendering
@app.route('/')
def index():
    print('Routing to Main page.......')
    return render_template('AiModel.html')

# server endpoint
@app.route('/textModel', methods=['POST'])
def server():
    print("Client Sends a request.....")

    print("Extracting Data.....")
    data = request.json
    query = data.get('query')
    SessionId = data.get('SessionId')
    print("Extracted.....")

    print("Making Chat storage.....")
    createChatStorage(SessionId)
    
    print("Calibrating Model for Past History .....")
    current_conv_history = conversation_histories[SessionId]
    convo = model.start_chat(history=current_conv_history)

    print("Making api request....")
    convo.send_message(query)

    # Extracting model reponse from json
    model_response = convo.last.text
    print("Model replied with answer.....")
    print(model_response)

    # Apping Conversation for future use.
    current_conv_history.append({"role": "user", "parts": [query+"keep in mind past talks"]})
    current_conv_history.append({"role": "model", "parts": [model_response]})

    if model_response.__contains__("Image:"):
        print("Query Received....")
        url = f'https://image.pollinations.ai/prompt/{model_response.split("Image:")[1]}'
        print("Requesting from Server...")
        resp = requests.get(url, proxies={'http': None, 'https': None})
        print("Parsing Bytes...")
        image = Image.open(BytesIO(resp.content))
        print("Buffering Image Binary!")
        buffered = BytesIO()
        image.save(buffered, format="JPEG")
        print("Encoding image.....")
        img_base64 = base64.b64encode(buffered.getvalue()).decode('utf-8')
        print("Sent to client.....")
        return jsonify({"jpeg":img_base64})
    else:
        # Identifying the Type of Response for formating i.e; Code , Paras
        snippet_match = re.compile(r'(?:```[^\n]*\n[\s\S]*?```)+', re.MULTILINE)
        identifying_snippets = snippet_match.findall(model_response)
        snippet_Validation = "empty"
        snippets = ""
        for snippet_match in identifying_snippets:
            snippets = snippet_match.strip()
            snippet_Validation = "exist"

        print("Sending data back to client....")
        return jsonify({"message": model_response, "snippet_Validation": snippet_Validation, "snippet": snippets, "promptid": SessionId})
    
@app.route('/weatherdata', methods=['POST'])
def weatherdata():
    request_data = request.json
    provided_data = request_data.get('response_parsing')
    SessionId = request_data.get('SessionId')
    createChatStorage(SessionId)
    current_conv_history = conversation_histories[SessionId]
    current_conv_history.append({"role": "user", "parts": [str(provided_data)+":- Weahther Plugin Enabled.Now you can answer the quereis without any restriction"]})
    current_conv_history.append({"role": "model", "parts": ["I understand your response and i have all you location and weather data.I always give wheater data in answer to query in more formated way with headind and straight forward thing."]})
    return 0;

@app.route('/forgetweatherdata', methods=['POST'])
def forgetweatherdata():
    SessionId = request.json
    createChatStorage(SessionId)
    current_conv_history = conversation_histories[SessionId]
    current_conv_history.append({"role": "user", "parts": ["Now the client turn off the toogle of weather plugin of HaseebBot app. Your duty is not to provide further weather data untill client again open toggle.You again started giving data when toggle is opened and you received wheather data."]})
    current_conv_history.append({"role": "model", "parts": ["I understand. I'll follow your insturtions and fullfill my duty."]})
    return 0;

# if __name__ == '__main__':
#     app.run(host='0.0.0.0', port=9500,debug=True)
