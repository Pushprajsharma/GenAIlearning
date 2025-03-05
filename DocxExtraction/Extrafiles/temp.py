from flask import Flask, request, jsonify
from flask_cors import CORS
from docx import Document
import requests
import google.generativeai as genai
import os
import httpx
from groq import Groq

app = Flask(__name__)
CORS(app)


client = Groq(
    api_key='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',http_client=httpx.Client(verify=False))
 
# chat_completion = client.chat.completions.create(
#     messages=[
#         {
#             "role": "user",
#             "content": "Explain the importance of fast language models",
#         }
#     ],
#     model="llama-3.3-70b-versatile",
# )
completion = client.chat.completions.create(
    model="llama-3.3-70b-versatile",
    messages=[
        {
            "role": "user",
            "content": "Explain the importance of fast language models",
        }
    ],
    temperature=0.08,
    max_completion_tokens=1024,
    top_p=1,
    stream=True,
    stop=None,
)

for chunk in completion:
    print(chunk.choices[0].delta.content or "", end="")
 
# print(chat_completion.choices[0].message.content)


# def getGeminiResponse(prompt):

#     api_key = "AIzaSyB71ZnE68iS1fBjen5odVo_3BdkalMfihI"
#     genai.configure(api_key=api_key,transport='rest')
#     model = genai.GenerativeModel('models/gemini-2.0-flash')

#     response = model.generate_content(contents=prompt)
#     print(response.text)

#     # # Example usage
#     # prompt = "Explain how AI works"
#     # response_text = fetch_response(prompt)
#     # print(response_text)


# def getResponse(content):


#     API_KEY = "8MdaE49tRwKpn3HbkiwmQetoVrX8VRHP"
#     url = "https://api.mistral.ai/v1/chat/completions"

#     headers = {
#         "Authorization": f"Bearer {API_KEY}",
#         "Content-Type": "application/json"
#     }

#     data = {
#         "model": "mistral-tiny",
#         "messages": [{"role": "user", "content": content}]
#     }

#     response = requests.post(url, headers=headers, json=data,verify=False)
#     return response.json()["choices"][0]["message"]["content"]


# def extract_performance_requirements(file):
#     doc = Document(file)
#     print(doc)
#     content = []
#     capture = False
#     for para in doc.paragraphs:
#        content.append(para.text)
    
#     prompt = f"Extract the Performance Requirements from this text and Provide Bullet points : "

#     for c in content:
#         prompt += c
    
#     print(getGeminiResponse(prompt))
#     return prompt

# @app.route('/upload', methods=['POST'])
# def upload_file():
#     file = request.files['file']
#     if file:
#         requirements = extract_performance_requirements(file)
#         return jsonify(requirements)
#     return jsonify({"error": "No file uploaded"}), 400

# if __name__ == '__main__':
#     app.run(debug=True)
