from flask import Flask, request, jsonify, send_file
from rembg import remove
from flask_cors import CORS
from io import BytesIO

app = Flask(__name__)
CORS(app)  # Enable CORS for all origins

@app.route('/remove_background', methods=['POST'])
def remove_background():
    if 'file' not in request.files:
        return jsonify({'success': False, 'error': 'No file provided'})

    file = request.files['file']

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

    return jsonify({'success': False, 'error': 'Error processing file'})

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))  # Use the PORT environment variable or default to 5000
    app.run(host="0.0.0.0", port=port, debug=True)