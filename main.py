import os
import logging
from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from rembg import remove
from io import BytesIO

app = Flask(__name__)

# CORS configuration
CORS(app, resources={r"/*": {"origins": "*"}})  # Allow all origins

# Configure logging
logging.basicConfig(level=logging.INFO)  # Set to DEBUG for more detailed logs
logger = logging.getLogger(__name__)


@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'healthy'}), 200


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


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))  # Use PORT environment variable if available
    app.run(host='0.0.0.0', port=port)
