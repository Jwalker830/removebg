import os
import logging
import threading
import time
from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from rembg import remove
from io import BytesIO

app = Flask(__name__)

# CORS configuration
CORS(app, resources={r"/*": {"origins": "*"}})  # Allow all origins

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'healthy'}), 200


@app.route('/', methods=['POST'])
def remove_background():
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


def background_task():
    while True:
        # Perform some periodic task
        logger.info("Background task is running...")
        time.sleep(60)  # Sleep for 60 seconds before running the task again


if __name__ == '__main__':
    # Start the background task in a separate thread
    threading.Thread(target=background_task, daemon=True).start()

    # Run the Flask app
    port = int(os.environ.get('PORT', 5000))  # Use PORT environment variable if available
    app.run(host='0.0.0.0', port=port)
