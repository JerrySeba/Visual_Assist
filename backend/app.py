import os
import io
from flask import Flask, request, jsonify
from flask_cors import CORS
from google.cloud import vision
from dotenv import load_dotenv

# 1. Setup & Configuration
load_dotenv()
app = Flask(__name__)
CORS(app) # Allows your HTML/Android frontend to talk to this server

# Initialize Google Vision Client
# It automatically looks for the GOOGLE_APPLICATION_CREDENTIALS env var
client = vision.ImageAnnotatorClient()

# 2. Helper Function: Process Image based on Mode
def analyze_image(image_content, mode):
    image = vision.Image(content=image_content)
    
    if mode == 'text':
        # OCR Mode: For "Read Text" button
        response = client.text_detection(image=image)
        annotations = response.text_annotations
        return annotations[0].description if annotations else "No text detected."

    elif mode == 'diagram':
        # Label/Object Detection: For "Explain Diagram" button
        # We combine Labels and Objects to "understand" the diagram
        response = client.label_detection(image=image)
        labels = [label.description for label in response.label_annotations]
        return f"This looks like a diagram containing: {', '.join(labels[:5])}."

    elif mode == 'navigation':
        # Object Detection: For "Navigation & People" button
        response = client.object_localization(image=image)
        objects = [obj.name for obj in response.localized_object_annotations]
        if not objects:
            return "The path ahead looks clear."
        return f"I see the following in your path: {', '.join(set(objects))}."

    return "Unknown mode selected."

# 3. API Endpoints
@app.route('/api/assist', methods=['POST'])
def assist():
    try:
        # Check if image and mode are provided
        if 'image' not in request.files or 'mode' not in request.form:
            return jsonify({"error": "Missing image or mode"}), 400

        image_file = request.files['image']
        mode = request.form['mode'] # 'text', 'diagram', or 'navigation'
        
        print(f"Processing request in {mode} mode...")
        
        # Read file into memory
        content = image_file.read()
        
        # Get AI Insights
        result_text = analyze_image(content, mode)
        
        return jsonify({
            "status": "success",
            "mode": mode,
            "description": result_text,
            "timestamp": "Just now"
        })

    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/status', methods=['GET'])
def status():
    return jsonify({"server": "active", "model": "Google Vision V1"})

if __name__ == '__main__':
    port = int(os.getenv('PORT', 3000))
    print(f"🚀 VisualAssist Backend running on port {port}")
    app.run(host='0.0.0.0', port=port, debug=True)