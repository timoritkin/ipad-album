import os
from flask import Flask, render_template, send_from_directory, send_file, abort

app = Flask(__name__, static_folder='static', template_folder='templates')

# Path to the folder that contains photos (relative to this file)
PHOTO_DIR = os.path.join(app.static_folder, 'photos')

@app.route('/')
def index():
    # List image and video files (jpg, jpeg, png, gif, mp4, webm, ogv)
    media_files = [f for f in os.listdir(PHOTO_DIR) if f.lower().endswith(('.jpg', '.jpeg', '.png', '.gif', '.mp4', '.webm', '.ogv'))]
    # Sort alphabetically
    media_files.sort()
    return render_template('index.html', media=media_files)

# Serve photos from static/photos directory
@app.route('/photos/<path:filename>')
def photos(filename):
    """Serve image or video files with correct MIME type and support HTTP range requests.
    iOS Safari (especially older versions) requires proper Content-Type and
    support for partial content (206) to play videos smoothly.
    """
    import mimetypes, os
    file_path = os.path.join(PHOTO_DIR, filename)
    if not os.path.isfile(file_path):
        abort(404)
    # Guess MIME type; fallback to generic binary
    mime_type, _ = mimetypes.guess_type(file_path)
    if mime_type is None:
        mime_type = 'application/octet-stream'
    # Use Flask's send_file with conditional=True to enable range requests
    return send_file(file_path, mimetype=mime_type, conditional=True)


if __name__ == '__main__':
    # Use host 0.0.0.0 so it is reachable on the local network
    app.run(host='0.0.0.0', port=5000, debug=False)
