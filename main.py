import os
import logging
import signal
import sys
import threading
from flask import Flask, request, jsonify, send_file, Response
from flask_cors import CORS
from rembg import remove
from io import BytesIO
from PIL import Image
import time

app = Flask(__name__)

# CORS configuration
CORS(app, resources={r"/*": {"origins": "*"}})  # Allow all origins

# Configure logging
logging.basicConfig(level=logging.INFO)  # Set to DEBUG for more detailed logs
logger = logging.getLogger(__name__)

# Graceful shutdown handling
def handle_shutdown(signum, frame):
    logger.info(f"Received shutdown signal: {signum}. Shutting down gracefully...")
    sys.exit(0)

signal.signal(signal.SIGTERM, handle_shutdown)
signal.signal(signal.SIGINT, handle_shutdown)

def create_blank_favicon():
    # Create a 1x1 pixel image
    img = Image.new('RGBA', (1, 1), color=(0, 0, 0, 0))  # Transparent 1x1 image
    buf = BytesIO()
    img.save(buf, format='PNG')
    buf.seek(0)
    return buf

@app.route('/favicon.ico')
def favicon():
    img = create_blank_favicon()
    return Response(img, mimetype='image/x-icon')  # Use 'image/x-icon' for favicon

# Top-level error handler
@app.errorhandler(Exception)
def handle_exception(e):
    """Handle unexpected errors."""
    logger.error(f"An unexpected error occurred: {e}", exc_info=True)
    return jsonify({'success': False, 'error': 'An unexpected error occurred. Please try again later.'}), 500

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint."""
    return jsonify({"status": "healthy"}), 200

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        return jsonify({"Choo Choo": "Welcome to your Flask app 🚅"})
    elif request.method == 'POST':
        if 'file' not in request.files:
            logger.error('No file provided')
            return jsonify({'success': False, 'error': 'No file provided'})

        file = request.files['file']

        try:
            if file:
                # Read the image file as bytes
                image_bytes = file.read()

                # Process the image using rembg
                processed_image = remove(image_bytes)

                # Create a BytesIO object to hold the processed image
                buffered = BytesIO(processed_image)
                buffered.seek(0)

                # Return the processed image file directly
                return send_file(
                    buffered,
                    mimetype='image/png',  # Adjust MIME type based on the output format
                    as_attachment=False,
                    download_name='processed_image.png'  # Optional: Specify the name of the file for download
                )
            else:
                logger.error('No file uploaded')
                return jsonify({'success': False, 'error': 'No file uploaded'})

        except Exception as e:
            logger.error(f'Error processing file: {e}')
            return jsonify({'success': False, 'error': str(e)})

# Background task
def background_task():
    while True:
        logger.info("Background task is running...")
        # Your code to execute when there are no requests
        time.sleep(10)  # Sleep for 10 seconds between iterations

# Start the background task in a separate thread
thread = threading.Thread(target=background_task)
thread.daemon = True
thread.start()

#if __name__ == '__main__':
#    port = int(os.environ.get('PORT', 8080))  # Changed port to 8080
#    app.run(host='0.0.0.0', port=port)
