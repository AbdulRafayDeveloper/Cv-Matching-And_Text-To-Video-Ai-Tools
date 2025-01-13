from flask import Flask, send_from_directory
from flask_cors import CORS
from routes.cvDetectRoutes import cvAPI
from routes.textToVideoRoutes import textToVideoAPI

app = Flask(__name__)

# Set the upload folder configurations
app.config['UPLOAD_FOLDER_CV'] = 'public/assets/cv'  # For CVs
app.config['UPLOAD_FOLDER_VIDEOS'] = 'public/assets/videos'  # For Videos
app.config['UPLOAD_FOLDER_Tranformed_Images'] = 'public/assets/transformedImages' # For Transformed Images
app.config['UPLOAD_FOLDER_pdfCompression'] = 'public/assets/pdfCompression' # For Transformed Images
app.config['UPLOAD_FOLDER'] = 'public/uploads'
app.config['PUBLIC_FOLDER'] = 'public'

CORS(app, resources={r"/*": {"origins": "http://localhost:4000"}})

# Register the blueprint -- API Routes
app.register_blueprint(cvAPI) 
app.register_blueprint(textToVideoAPI)

if __name__ == "__main__":
    app.run(debug=True, port=8000)
