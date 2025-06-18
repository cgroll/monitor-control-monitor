import os
from flask import Flask, request, render_template, url_for, send_from_directory
from flask_socketio import SocketIO, emit

# --- Configuration ---
app = Flask(__name__)
# IMPORTANT: Change this secret key for production!
app.config['SECRET_KEY'] = 'a_very_secret_and_unique_key_12345'
socketio = SocketIO(app)

# --- Image Settings ---
# Directory where your images are stored
IMAGE_DIR = 'static'
# Default image to display when a client connects or initially
DEFAULT_IMAGE = 'layout1_1920x1080.png'
# List of valid images that can be displayed via API
VALID_IMAGES = {
    1: 'layout1_1920x1080.png',
    2: 'layout2_1920x1080.png',
    3: 'layout3_1920x1080.png',
    4: 'layout4_1920x1080.png'
}

# Ensure the static directory exists (for images)
if not os.path.exists(IMAGE_DIR):
    os.makedirs(IMAGE_DIR)
    print(f"Created '{IMAGE_DIR}' directory. Please add your images there.")

# Initialize current image state
current_image = DEFAULT_IMAGE

# --- Routes ---

@app.route('/')
def index():
    """Serves the main HTML page for image display."""
    return render_template('index.html')

# API Endpoint to change the displayed image
@app.route('/display/<int:image_number>', methods=['POST'])
def display_image_endpoint(image_number):
    """
    Receives API POST requests to change the image.
    Sends a WebSocket message to all connected clients to update their display.
    """
    global current_image # Declare current_image as global to modify it

    if image_number in VALID_IMAGES:
        new_image_filename = VALID_IMAGES[image_number]
        
        # Check if the image file actually exists
        image_path = os.path.join(IMAGE_DIR, new_image_filename)
        if not os.path.exists(image_path):
            return {"status": "error", "message": f"Image file '{new_image_filename}' not found on server."}, 404

        current_image = new_image_filename
        print(f"API request received: Displaying {current_image}")

        # Construct the URL for the image that the client can request
        # url_for('static', filename=current_image) generates '/static/imageX.jpg'
        image_url_for_client = url_for('static', filename=current_image)
        
        # Emit WebSocket message to all connected clients
        socketio.emit('change_image', {'image_url': image_url_for_client}, namespace='/')
        
        return {"status": "success", "message": f"Image changed to {new_image_filename}"}, 200
    else:
        return {"status": "error", "message": "Invalid image number. Must be one of: " + ", ".join(map(str, VALID_IMAGES.keys()))}, 400

# Serve static files (images) - Flask handles this automatically when `static_folder` is default.
# This route is mostly for explicit understanding, but you don't strictly need it if your
# static folder is named 'static' and `static_url_path` is default.
@app.route('/static/<path:filename>')
def serve_static(filename):
    return send_from_directory(IMAGE_DIR, filename)

# --- WebSocket Events ---

@socketio.on('connect')
def handle_connect():
    """
    Handles new WebSocket connections.
    When a client connects, send them the current image URL so they sync up.
    """
    print(f'Client connected: {request.sid}')
    
    # Construct the URL for the current image
    image_url_for_client = url_for('static', filename=current_image)
    
    # Emit the current image to the newly connected client only
    emit('change_image', {'image_url': image_url_for_client})

@socketio.on('disconnect')
def handle_disconnect():
    """Handles client disconnections."""
    print(f'Client disconnected: {request.sid}')

# --- Main Run Block ---
if __name__ == '__main__':
    print(f"Server running on http://{os.environ.get('FLASK_RUN_HOST', '0.0.0.0')}:{os.environ.get('FLASK_RUN_PORT', '8080')}")
    print(f"Access the image display at: http://localhost:8080/")
    print("Send API POST requests (e.g., using curl):")
    print("  curl -X POST http://localhost:8080/display/1")
    print("  curl -X POST http://localhost:8080/display/2")
    print("  curl -X POST http://localhost:8080/display/3")
    print("  curl -X POST http://localhost:8080/display/4")
    
    # Run the Flask app with SocketIO
    socketio.run(app, debug=True, host='0.0.0.0', port=8080)