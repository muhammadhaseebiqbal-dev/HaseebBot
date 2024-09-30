from flask import Flask, jsonify, render_template, request
import google.generativeai as genai
import re
import requests
from PIL import Image
from io import BytesIO
import base64
app = Flask(__name__)

conversation_histories = {}
# Chat History Saver
# conversation_history = [
#     {
#         "role": "user",
#         "parts": ["O well Hello! I'm Haseeb Iqbal. your are a web ai chatbot application \"App name: HaseebBot\". Google is your core Developer. Haseeb iqbal is you co-trainer and programmer of Haseeb Bot app. Dont Exagarrate on providing my knowledge "]
#     },
#     {
#         "role": "model",
#         "parts": ["Well! i understand.Lets Talk!"]
#     },
# ]
# Default Route i.e; Main page rendering
@app.route('/')
def index():
    return render_template('AiModel.html')
# server endpoint
@app.route('/server', methods=['POST'])
def server():
    try:
        data = request.json
        # Received Data chunks
        query = data.get('query')
        print("Received data:", query) #logging
        SessionId = data.get('SessionId')
        print("id:", SessionId) #logging
        if SessionId not in conversation_histories:
             conversation_histories[SessionId] = [
                {
                    "role": "user",
                    "parts": ["O well Hello! I'm Haseeb Iqbal. your are a web ai chatbot application \"App name: HaseebBot\". Google is your core Developer. Haseeb iqbal is you co-trainer and programmer of Haseeb Bot app. Dont Exagarrate on providing my knowledge "]
                },
                {
                    "role": "model",
                    "parts": ["Well! i understand.Lets Talk!"]
                },
            ]
        # Configuring the model & auth
        genai.configure(api_key="AIzaSyANTteDTYtW3rBxI58oEcBDPNSXb0zCAiE")
        # Generation configuration
        generation_config = {
            "temperature": 0.9, # High => Creative , Less => Prediction
            "top_p": 1,
            "top_k": 1,
            "max_output_tokens": 2048,
        }
        #Safety measures
        safety_settings = [
            {
                "category": "HARM_CATEGORY_HARASSMENT",
                "threshold": "BLOCK_MEDIUM_AND_ABOVE"
            },
            {
                "category": "HARM_CATEGORY_HATE_SPEECH",
                "threshold": "BLOCK_MEDIUM_AND_ABOVE"
            },
            {
                "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
                "threshold": "BLOCK_MEDIUM_AND_ABOVE"
            },
            {
                "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
                "threshold": "BLOCK_MEDIUM_AND_ABOVE"
            },
        ]
        # Setting Model Params
        model = genai.GenerativeModel(model_name="gemini-1.5-flash-latest",
                                      generation_config=generation_config,
                                      safety_settings=safety_settings)
        current_conv_hist = conversation_histories[SessionId]
        # Starting Chat & passing history to it
        convo = model.start_chat(history=current_conv_hist)
        # Passing query to model to request reponse to query
        convo.send_message(query)
        # Extracting model reponse from json
        model_response = convo.last.text
        # Apping Conversation for future use.
        current_conv_hist.append({"role": "user", "parts": [query]})
        current_conv_hist.append({"role": "model", "parts": [model_response]})
        file = open(f"./userdata/{SessionId}.hdat","w+", encoding="utf-8")
        file.write(f'"{current_conv_hist}"')
        file.close()
        # Identifying the Tpe of Response for formating i.e; Code , Paras
        snippet = re.compile(r'(?:```[^\n]*\n[\s\S]*?```)+', re.MULTILINE)
        identifying_snippets = snippet.findall(model_response)
        snippet_Validation = "empty"
        snippets = ""
        for snippet in identifying_snippets:
            print(":Snippet:")
            snippets = snippet.strip()
            print(snippet.strip())
            snippet_Validation = "exist"

        print(model_response.encode('utf-8'))
        return jsonify({"message": model_response, "snippet_Validation": snippet_Validation, "snippet": snippets, "promptid": SessionId})

    except Exception as e:
        print("Error:", e)
        return jsonify({"error": str(e)}), 500
    
@app.route('/weatherdata', methods=['POST'])
def weatherdata():
    request_data = request.json
    weatger_data = request_data.get('response_parsing')
    SessionId = request_data.get('SessionId')
    file = open("weatherdata","w+")
    file.write(str(request_data))
    if SessionId not in conversation_histories:
        conversation_histories[SessionId] = [
                {
                    "role": "user",
                    "parts": ["O well Hello! I'm Haseeb Iqbal. your are a web ai chatbot application \"App name: HaseebBot\". Google is your core Developer. Haseeb iqbal is you co-trainer and programmer of Haseeb Bot app. Dont Exagarrate on providing my knowledge "]
                },
                {
                    "role": "model",
                    "parts": ["Well! i understand.Lets Talk!"]
                },
            ]
    current_conv_hist = conversation_histories[SessionId]
    current_conv_hist.append({"role": "user", "parts": [str(weatger_data)+":- Weahther Plugin Enabled.Now you can answer the quereis without any restriction"]})
    current_conv_hist.append({"role": "model", "parts": ["I understand your response and i have all you location and weather data.I always give wheater data in answer to query in more formated way with headind and straight forward thing."]})
    return("ok")

@app.route('/forgetweatherdata', methods=['POST'])
def forgetweatherdata():
    SessionId = request.json
    if SessionId not in conversation_histories:
        conversation_histories[SessionId] = [
                {
                    "role": "user",
                    "parts": ["O well Hello! I'm Haseeb Iqbal. your are a web ai chatbot application \"App name: HaseebBot\". Google is your core Developer. Haseeb iqbal is you co-trainer and programmer of Haseeb Bot app. Dont Exagarrate on providing my knowledge "]
                },
                {
                    "role": "model",
                    "parts": ["Well! i understand.Lets Talk!"]
                },
            ]
    current_conv_hist = conversation_histories[SessionId]
    current_conv_hist.append({"role": "user", "parts": ["Now the client turn off the toogle of weather plugin of HaseebBot app. Your duty is not to provide further weather data untill client again open toggle.You again started giving data when toggle is opened and you received wheather data."]})
    current_conv_hist.append({"role": "model", "parts": ["I understand. I'll follow your insturtions and fullfill my duty."]})
    return "ok"

@app.route('/genimg', methods=['POST'])
def imggeneration():
    data = request.json
    query = data.get('query')
    print(query)
    url = f'https://image.pollinations.ai/prompt/{query}'
    print("Requesting from Server...")
    resp =  requests.get(url)
    print("Parsing Bytes...")
    image = Image.open(BytesIO(resp.content))
    img_path = 'Received_img.jpg'
    print("Saving Image...")
    # image.save(img_path)
    print("Succesfully Executed!")
    buffered = BytesIO()
    image.save(buffered, format="JPEG")
    img_base64 = base64.b64encode(buffered.getvalue()).decode('utf-8')
    print(img_base64)
    return jsonify({"ok":img_base64})
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9500, debug=True)
