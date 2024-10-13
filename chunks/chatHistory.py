conversation_histories = {}
def createChatStorage(SessionId):
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
            {
                "role": "user",
                "parts": ["hi gemini",],
            },
            {
                "role": "model",
                "parts": ["Hi! What can I do for you today? \n",],
            },
            {
                "role": "user",
                "parts": ["This is HaseebAi web app. and i want you to understand my logic. im using your api and requesting you the answers of prompt form my web app . I want that when user ask to generate image in prompt given by use . you must answer it in this format \"Image : {summary of whole prompt given by user}\" and if it doesnt ask to generate image you must answer it as regular",],
            },
            {
                "role": "model",
                "parts": ["I understand! Let's get this working. \n\nHere's how I'll process your requests based on your logic:\n\n1. **Identify Image Generation Requests:** \n   - I'll analyze the user's prompt.\n   - If the prompt includes keywords or phrases commonly associated with image generation (e.g., \"generate an image of\", \"create a picture of\", \"draw a...\", \"imagine a...\", etc.), I'll understand it's an image generation request.\n\n2. **Format the Response:**\n   - **Image Generation:** If I detect an image generation request, my response will follow this format:\n     ```json\n     {\n       \"Image\": \"{Summary of the entire user prompt}\"\n     }\n     ```\n   - **Non-Image Generation:** If it's not an image generation request, I'll respond as a regular text-based response. \n\n**Example:**\n\n**User Prompt:** \"Generate a picture of a cat wearing a hat in a field of flowers.\"\n\n**My Response:**\n```json\n{\n  \"Image\": \"A cat wearing a hat in a field of flowers.\"\n}\n```\n\n**User Prompt:** \"What is the capital of France?\"\n\n**My Response:** \"The capital of France is Paris.\" \n\n**Important Considerations:**\n\n* **Specificity:** Make sure the prompt clearly indicates image generation intent to avoid ambiguity.\n* **API Integration:** You'll need to integrate the image generation API to process the \"Image\" response and generate the actual image. \n\nLet me know if you have any more questions or want to test this out with more examples. \n",],
            },
            {
                "role": "user",
                "parts": ["generate an image of cowboy"],
            },
            {
                "role": "model",
                "parts": ["```json\n{\n  \"Image\": \"A cowboy, rugged and tough, in a wide-brimmed hat, leather boots, and a denim jacket. He might be riding a horse, holding a lasso, or standing tall with a determined look on his face.\"\n}\n``` \n"],
            },
            {
                "role": "user",
                "parts": ["give me without any json structure only give me in string",],
            },
            {
                "role": "model",
                "parts": ["Image: A cowboy, rugged and tough, in a wide-brimmed hat, leather boots, and a denim jacket. He might be riding a horse, holding a lasso, or standing tall with a determined look on his face. \n",],
            },
            {
                "role": "user",
                "parts":["genrate a pic of bcat with mouse having lunck"]
            },
            {
                "role": "model",
                "parts":["json\"Image\": \"{A bcat, with its signature blue fur and big, round eyes, sitting at a small table with a mouse. The mouse is wearing a tiny chef's hat and is holding a plate with a miniature, gourmet meal, perhaps a tiny steak or a tiny piece of cheese. The bcat is looking at the mouse with a playful and slightly mischievous expression, as if it is about to pounce on the mouse and steal its lunch.}"]
            },
            {
                "role": "user",
                "parts":["why you are give in json give me resp as i tell you before"]
            },
            {
                "role": "user",
                "parts":["Image: A bcat, with its signature blue fur and big, round eyes, sitting at a small table with a mouse. The mouse is wearing a tiny chef's hat and is holding a plate with a miniature, gourmet meal, perhaps a tiny steak or a tiny piece of cheese. The bcat is looking at the mouse with a playful and slightly mischievous expression, as if it is about to pounce on the mouse and steal its lunch."]
            },
        ]
