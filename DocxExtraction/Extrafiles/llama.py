from transformers import AutoModelForCausalLM, AutoTokenizer
import os

os.environ['TRANSFORMERS_OFFLINE'] = '1'


# Load the tokenizer and model
model_name = "meta-llama/Llama-2-7b-chat-hf"  # Replace with the desired model
tokenizer = AutoTokenizer.from_pretrained(model_name,trust_remote_code=True)
model = AutoModelForCausalLM.from_pretrained(model_name,trust_remote_code=True)


# Define your prompt
prompt = "Explain how artificial intelligence works."

# Tokenize the input
inputs = tokenizer(prompt, return_tensors="pt")

# Generate a response
outputs = model.generate(**inputs, max_length=100)

# Decode and print the response
response = tokenizer.decode(outputs[0], skip_special_tokens=True)
print(response)
