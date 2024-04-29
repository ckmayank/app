import os
import google.generativeai as genai
from flask import Flask, render_template, request
from PIL import Image

app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = 'uploads'

# Attempting to retrieve the Google API key from user-specific data
api_key = 'AIzaSyA1PdbBzPFkf10UDewNv9kZSAWr2Lp60h4'

# Configuring the genai module with the obtained API key for authentication
genai.configure(api_key=api_key)

# Creating an instance of the GenerativeModel class with the model name 'gemini-pro-vision'
model = genai.GenerativeModel('gemini-pro-vision')

def process_frame(image_path):
    pil_image = Image.open(image_path)
    return pil_image

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    if 'file' not in request.files:
        return '', 400

    file = request.files['file']
    if not file:
        return '', 400

    filename = 'capture.png'
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(filepath)

    # Processing the uploaded image
    processed_image = process_frame(filepath)

    # A text prompt describing the task to be performed on the provided image
    prompt = '''The provided image contains a book with a front page. Please extract the sentence and letter correctly.'''

    # Generating content using a model, passing the prompt and the image
    response = model.generate_content([prompt, processed_image])

    # Resolving the response to obtain the generated text
    response.resolve()

    # Stripping any leading or trailing whitespace from the generated text
    generated_text = response.text.strip()

    os.remove(filepath)
    print(generated_text)

    return generated_text

if __name__ == '__main__':
    app.run(debug=False)
