from flask import Flask, jsonify, render_template, request
import google.generativeai as genai
import re
import requests
from PIL import Image
from io import BytesIO
import base64
from better_profanity import profanity
from twilio.rest import Client

app = Flask(__name__)

# twilio config
account_sid = 'ACcd3195d5143ca1e9f29260b009bb1b36'
auth_token = 'a58861c49c21589120860f738c6163f2'
client = Client(account_sid, auth_token)

conversation_histories = {}

# Default Route i.e; Main page rendering
@app.route('/')
def index():
    print('Routing to Main page.......')
    return render_template('AiModel.html')
# server endpoint
@app.route('/server', methods=['POST'])
def server():
    data = request.json
    ismsg = data.get('msgquery')
    if not ismsg :
        try:
            print("Client Sends a request.....")

            print("Extracting Data.....")
            query = data.get('query')
            SessionId = data.get('SessionId')
            print("Extracted.....")

            print("Making Chat storage.....")
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
            

            print("Configuring the model.....")
            genai.configure(api_key="AIzaSyANTteDTYtW3rBxI58oEcBDPNSXb0zCAiE")
            generation_config = {
                "temperature": 0.9, # High => Creative , Less => Prediction
                "top_p": 1,
                "top_k": 1,
                "max_output_tokens": 2048,
            }
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
            
            print("Configuration Done.....")

            print("Calibrating Model.....")
            current_conv_hist = conversation_histories[SessionId]
            convo = model.start_chat(history=current_conv_hist)
            # Passing query to model to request reponse to query
            convo.send_message(query)
            # Extracting model reponse from json
            model_response = convo.last.text
            print("Model replied with answer.....")
            # Apping Conversation for future use.
            current_conv_hist.append({"role": "user", "parts": [query]})
            current_conv_hist.append({"role": "model", "parts": [model_response]})
            # Identifying the Type of Response for formating i.e; Code , Paras
            snippet = re.compile(r'(?:```[^\n]*\n[\s\S]*?```)+', re.MULTILINE)
            identifying_snippets = snippet.findall(model_response)
            snippet_Validation = "empty"
            snippets = ""
            for snippet in identifying_snippets:
                snippets = snippet.strip()
                snippet_Validation = "exist"

            print("Sending data back to client....")
            return jsonify({"message": model_response, "snippet_Validation": snippet_Validation, "snippet": snippets, "promptid": SessionId})

        except Exception as e:
            print("Error:", e)
            return jsonify({"error": str(e)}), 500
    else:
        query = data.get('query')
        number = re.search(r"\+92\d{10,12}", query)
        print(query.split("that")[len(query.split("that"))-1])
        message = client.messages.create(
            from_='whatsapp:+14155238886',
            content_sid='HX5c7345a81cf39c02bf554ecd89d5b549',
            content_variables=f'{{"1":"{query.split("that")[len(query.split("that"))-1]} "}}',
            to=f'whatsapp:{number.group()}'
        )
        return jsonify({"msg": "sent"})
    
@app.route('/weatherdata', methods=['POST'])
def weatherdata():
    request_data = request.json
    provided_data = request_data.get('response_parsing')
    SessionId = request_data.get('SessionId')
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
    current_conv_hist.append({"role": "user", "parts": [str(provided_data)+":- Weahther Plugin Enabled.Now you can answer the quereis without any restriction"]})
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
    profanity.load_censor_words
    if profanity.contains_profanity(query.replace('@ImgAi'," ")):
        return jsonify({"warning":"Ganday Bachey"})
    else:
        print("Query Received....")
        url = f'https://image.pollinations.ai/prompt/{query}'
        print("Requesting from Server...")
        resp = requests.get(url, proxies={'http': None, 'https': None})
        print("Parsing Bytes...")
        image = Image.open(BytesIO(resp.content))
        print("Succesfully Executed!")
        buffered = BytesIO()
        image.save(buffered, format="JPEG")
        print("Encoding image.....")
        img_base64 = base64.b64encode(buffered.getvalue()).decode('utf-8')
        print("Sent to client.....")
        return jsonify({"jpeg":img_base64})

# if __name__ == '__main__':
#     app.run(host='0.0.0.0', port=9500,debug=True)