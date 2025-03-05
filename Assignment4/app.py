import json
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import make_pipeline
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Load JSON data
with open('qa_data.json') as f:
    data = json.load(f)

# Convert JSON data to a DataFrame
df = pd.DataFrame(data)

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(df['question'], df['answer'], test_size=0.2, random_state=42)

# Create a pipeline with TfidfVectorizer and Logistic Regression
qa_pipeline = make_pipeline(TfidfVectorizer(), LogisticRegression())

# Train the model
qa_pipeline.fit(X_train, y_train)

# Make predictions on the test set
y_pred = qa_pipeline.predict(X_test)

# Calculate accuracy
accuracy = accuracy_score(y_test, y_pred)
print(f"Accuracy: {accuracy}")

def answer_question(question):
    return qa_pipeline.predict([question])[0]

# # Example question
# question = "Capital of France"

# # Get the answer
# answer = answer_question(question)
# print(f"Question: {question}")
# print(f"Answer: {answer}")



@app.route('/ask', methods=['GET'])
def ask_question():
    question = request.args.get('q')
    if not question:
        return jsonify({'error': 'No question provided'}), 400
    answer = answer_question(question)
    return jsonify({'question': question, 'answer': answer})

if __name__ == '__main__':
    app.run(debug=True)
