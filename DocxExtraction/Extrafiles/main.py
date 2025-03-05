from flask import Flask, request, jsonify
from flask_cors import CORS
from docx import Document
import requests


app = Flask(__name__)
CORS(app)

# API_KEY = "8MdaE49tRwKpn3HbkiwmQetoVrX8VRHP"
# url = "https://api.mistral.ai/v1/chat/completions"

# headers = {
#     "Authorization": f"Bearer {API_KEY}",
#     "Content-Type": "application/json"
# }

# data = {
#     "model": "mistral-tiny",
#     "messages": [{"role": "user", "content": "How does AI work?"}]
# }

# response = requests.post(url, headers=headers, json=data,verify=False)
# print(response.json()["choices"][0]["message"]["content"])


def extract_performance_requirements(file):
    doc = Document(file)
    print(doc)
    content = []
    capture = False
    for para in doc.paragraphs:
        if "performance requirements" in para.text.lower():
            capture = True
            content.append(f'{para.text}')
        elif capture:
            if para.text.strip() == "":
                capture = False
            else:
                content.append(f'{para.text}')
        elif "performance requirements" in para.text.lower():
            content.append(f'{para.text}')
    return content

@app.route('/upload', methods=['POST'])
def upload_file():
    file = request.files['file']
    if file:
        requirements = extract_performance_requirements(file)
        return jsonify(requirements)
    return jsonify({"error": "No file uploaded"}), 400

if __name__ == '__main__':
    app.run(debug=True)
