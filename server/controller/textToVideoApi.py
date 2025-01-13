from flask import Blueprint, jsonify, request
import os
import requests
from gtts import gTTS
from moviepy import *  # Import everything from moviepy
from PIL import Image, ImageDraw, ImageFont
import logging
import numpy as np

UPLOAD_FOLDER_VIDEOS = 'public/assets/videos'
if not os.path.exists(UPLOAD_FOLDER_VIDEOS):
    os.makedirs(UPLOAD_FOLDER_VIDEOS)

UNSPLASH_ACCESS_KEY = 'vMiXDjg8xyXtZM-0Ra_udet6dNAhtQGVvzR3u0sdd8g'

def text_to_speech(text, filename='audio.mp3'):
    tts = gTTS(text)
    tts.save(filename)
    return filename

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

def download_image(query, filename='image.png'):
    url = f"https://api.unsplash.com/photos/random?query={query}&client_id={UNSPLASH_ACCESS_KEY}"
    response = requests.get(url)
    
    if response.status_code != 200:
        logging.error(f"Failed to fetch image: {response.status_code} - {response.text}")
        raise Exception(f"Failed to fetch image: {response.status_code} - {response.text}")

    data = response.json()

    if 'urls' not in data:
        logging.error(f"'urls' key not found in the response data: {data}")
        raise KeyError("'urls' key not found in the response data")

    image_url = data['urls']['regular']  # Use 'regular' size for better resolution

    image_response = requests.get(image_url)
    with open(filename, 'wb') as file:
        file.write(image_response.content)
    return filename

def overlay_text_on_image(image_path, text):
    image = Image.open(image_path).convert("RGBA")
    draw = ImageDraw.Draw(image)
    font = ImageFont.truetype("arial.ttf", size=40)
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width, text_height = bbox[2] - bbox[0], bbox[3] - bbox[1]
    position = ((image.width - text_width) // 2, (image.height - text_height) // 2)
    draw.text(position, text, fill=(255, 255, 255, 255), font=font)

    return image

def create_slideshow_video(image_files, text_parts, audio_file, output_file='output_video.mp4'):
    clips = []
    audio_clip = AudioFileClip(audio_file)
    audio_duration = audio_clip.duration
    duration_per_clip = audio_duration / len(image_files) if image_files else 0

    for image_file, text in zip(image_files, text_parts):
        # Create the ImageClip and set the duration
        image_clip = ImageClip(image_file).with_duration(duration_per_clip)

        # Optionally add text overlay
        if text:
            image_clip = image_clip.with_position("center").with_opacity(0.8)  # Adjust text opacity if needed

        clips.append(image_clip)

    # Concatenate all clips into a final video
    video = concatenate_videoclips(clips, method='compose')

    # Set audio to the video
    video = video.with_audio(audio_clip)

    # Write final video to file
    video.write_videofile(output_file, fps=24)

    return output_file

def convertIntoVideo():
    data = request.form
    text = data.get('text', '')

    if not text:
        return jsonify({'error': 'Text is required.'}), 400

    text_parts = text.split('.')
    image_files = []

    for i, part in enumerate(text_parts):
        filename = os.path.join(UPLOAD_FOLDER_VIDEOS, f'image_{i}.png')
        image_file = download_image(part.strip(), filename=filename)
        image_files.append(image_file)

    audio_file = text_to_speech(text, filename=os.path.join(UPLOAD_FOLDER_VIDEOS, 'audio.mp3'))
    video_file = create_slideshow_video(image_files, text_parts, audio_file, output_file=os.path.join(UPLOAD_FOLDER_VIDEOS, 'output_video.mp4'))

    return jsonify({'message': 'Video Created Successfully', 'status': 200})

textToVideoAPI = Blueprint('textToVideoAPI', __name__)
