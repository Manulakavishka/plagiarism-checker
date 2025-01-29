from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import os
import requests
from flask import Flask, request, jsonify
from flask_cors import CORS
import fitz  # PyMuPDF for PDF text extraction

app = Flask(__name__)
CORS(app)

# Function to extract text from PDF
def extract_text_from_pdf(file_path):
    doc = fitz.open(file_path)
    text = ""
    for page in doc:
        text += page.get_text()
    return text

# Function to perform plagiarism check (example using Copyleaks)
def check_plagiarism(text):
    api_url = "https://api.copyleaks.com/v3/education/scan"  # Example endpoint
    api_key = "your_copyleaks_api_key_here"  # Replace with your Copyleaks API key

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    # Send the text for plagiarism detection
    response = requests.post(api_url, headers=headers, json={"text": text})

    if response.status_code == 200:
        return response.json()  # Return the plagiarism check results
    else:
        return {"error": "Plagiarism check failed", "details": response.text}

# Function to calculate Cosine Similarity between two texts
def calculate_cosine_similarity(text1, text2):
    # Convert texts to TF-IDF vectors
    vectorizer = TfidfVectorizer(stop_words='english')
    tfidf_matrix = vectorizer.fit_transform([text1, text2])
    
    # Compute cosine similarity between the two vectors
    cosine_sim = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])
    return cosine_sim[0][0]

@app.route('/')
def home():
    return jsonify(message="Plagiarism Checker API is up!")

@app.route('/upload', methods=['POST'])
def upload_file():
    os.makedirs('uploads', exist_ok=True)
    
    # Get the uploaded file
    file = request.files['file']
    file_path = os.path.join('uploads', file.filename)
    
    # Save the file
    file.save(file_path)

    # Process the file (e.g., extract text from PDF)
    file_extension = file.filename.split('.')[-1].lower()
    if file_extension == 'pdf':
        text = extract_text_from_pdf(file_path)
    else:
        return jsonify(error="Only PDF files are supported for plagiarism check"), 400

    # Here, you would integrate your plagiarism detection logic
    # Perform plagiarism detection
    # plagiarism_result = check_plagiarism(text)
    
    # # For simplicity, we'll just return the extracted text
    # return jsonify(message="File uploaded and processed successfully", extracted_text=plagiarism_result)

 # Sample existing document text (could be any other document in your database)
    existing_text = "This is a sample text document that will be compared for plagiarism."

    # Calculate the similarity score
    similarity_score = calculate_cosine_similarity(text, existing_text)
    
    return jsonify(message="File uploaded and processed successfully", extracted_text=similarity_score)
    

if __name__ == '__main__':
    app.run(debug=True, port=5001)
