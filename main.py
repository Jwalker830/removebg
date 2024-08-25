from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from rembg import remove
from io import BytesIO

app = Flask(__name__)

# CORS configuration
CORS(app, resources={r"/*": {"origins": "*"}})  # Allow all origins

@app.route('/', methods=['POST'])
def remove_background():
    if 'file' not in request.files:
        return jsonify({'success': False, 'error': 'No file provided'})

    file = request.files['file']

    if file:
        image_bytes = file.read()
        processed_image = remove(image_bytes)
        buffered = BytesIO(processed_image)
        buffered.seek(0)

        return send_file(
            buffered,
            mimetype='image/png',
            as_attachment=False,
            download_name='processed_image.png'
        )

    return jsonify({'success': False, 'error': 'Error processing file'})

if __name__ == '__main__':
    app.run()
