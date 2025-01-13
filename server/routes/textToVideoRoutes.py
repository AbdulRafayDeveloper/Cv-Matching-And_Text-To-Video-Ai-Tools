from flask import Blueprint, send_from_directory
from controller.textToVideoApi import convertIntoVideo
textToVideoAPI = Blueprint('textToVideoAPI', __name__)

##### insert ######

@textToVideoAPI.route('/api/textToVideo', methods=['POST'])
def textToVideo_declare():
    return convertIntoVideo()