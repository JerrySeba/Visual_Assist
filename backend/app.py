import os
import io
from flask import Flask, request, jsonify
from flask_cors import CORS
from google.cloud import vision
from dotenv import load_dotenv

# 1. Load Environment Variables
# This will pick up GOOGLE_APPLICATION_CREDENTIALS and PORT from your .env file
load_dotenv()

app = Flask(__name__)
# Enable CORS so your frontend index.html can communicate with this API
CORS(app)

# 2. Initialize Google Vision Client
# The SDK automatically uses the path provided in GOOGLE_APPLICATION_CREDENTIALS
try:
    vision_client = vision.ImageAnnotatorClient()
    print("✅ Vision AI client initialized successfully.")
except Exception as e:
    print(f"❌ Failed to initialize Vision client: {e}")

def analyze_image(image_content, mode):
    """
    Core logic to handle different classroom assistance modes.
    """
    image = vision.Image(content=image_content)
    
    if mode == 'text':
        # OCR Mode for "Read Text" button
        response = vision_client.text_detection(image=image)
        annotations = response.text_annotations
        return annotations[0].description if annotations else "No text detected."

    elif mode == 'diagram':
        # Label detection to help explain charts/diagrams
        response = vision_client.label_detection(image=image)
        labels = [label.description for label in response.label_annotations]
        if not labels:
            return "I cannot identify the elements in this diagram."
        return f"This diagram contains: {', '.join(labels[:5])}."

    elif mode == 'navigation':
        # Object localization for "Navigation & People" button
        response = vision_client.object_localization(image=image)
        objects = [obj.name for obj in response.localized_object_annotations]
        if not objects:
            return "The path ahead looks clear."
        return f"I see the following in your path: {', '.join(set(objects))}."

    return "Invalid assistance mode selected."

# 3. API Endpoints
@app.route('/api/assist', methods=['POST'])
def assist():
    try:
        # Validate that the request has both an image and a mode
        if 'image' not in request.files or 'mode' not in request.form:
            return jsonify({
                "status": "error", 
                "message": "Missing image file or assistance mode"
            }), 400

        image_file = request.files['image']
        mode = request.form['mode']
        
        # Read the image binary data
        content = image_file.read()
        
        # Process image via Google Vision AI
        description = analyze_image(content, mode)
        
        return jsonify({
            "status": "success",
            "mode": mode,
            "description": description
        })

    except Exception as e:
        print(f"Server Error: {str(e)}")
        return jsonify({
            "status": "error", 
            "message": "An internal server error occurred."
        }), 500

@app.route('/status', methods=['GET'])
def health_check():
    return jsonify({"status": "active", "service": "VisualAssist Backend"})

# 4. Start Server
if __name__ == '__main__':
    # Uses PORT from .env (3000) or defaults to 5000 
    server_port = int(os.getenv('PORT', 3000))
    print(f"🚀 VisualAssist Server running on http://localhost:{server_port}")
    app.run(host='0.0.0.0', port=server_port, debug=True)
