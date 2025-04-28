from deepgram import DeepgramClient, PrerecordedOptions
import yt_dlp
import json
import os
import time
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get API key from environment variable
DEEPGRAM_API_KEY = os.getenv('DEEPGRAM_API_KEY')
if not DEEPGRAM_API_KEY:
    raise ValueError("Please set the DEEPGRAM_API_KEY environment variable")

# YouTube URL to process
YOUTUBE_URL = 'https://youtu.be/uBKDOBf1DVY?si=YunX3ATUdtAyt5P4'
OUTPUT_FILE = 'transcription.json'

def download_youtube_audio(url):
    """Download audio from YouTube URL and return the file path"""
    try:
        ydl_opts = {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
            'outtmpl': '%(title)s.%(ext)s',
        }
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            # Get the filename of the downloaded file
            filename = ydl.prepare_filename(info)
            # The actual file will have .mp3 extension due to postprocessing
            mp3_file = os.path.splitext(filename)[0] + '.mp3'
            return mp3_file
    except Exception as e:
        print(f"Error downloading audio: {str(e)}")
        return None

def main():
    # Download audio from YouTube
    print("Downloading audio from YouTube...")
    audio_file = download_youtube_audio(YOUTUBE_URL)
    if not audio_file:
        print("Failed to download audio. Exiting.")
        return
    print(f"Audio downloaded to: {audio_file}")

    # Initialize Deepgram client
    deepgram = DeepgramClient(DEEPGRAM_API_KEY)

    with open(audio_file, 'rb') as buffer_data:
        payload = { 'buffer': buffer_data }

        options = PrerecordedOptions(
            smart_format=True,
            model="nova-3",
            language="en-US",
            diarize=True  # Enable speaker diarization
        )

        print("Transcribing audio with Deepgram...")
        # Use the new recommended method
        response = deepgram.listen.rest.v("1").transcribe_file(payload, options)
        
        # Save response to file
        with open(OUTPUT_FILE, 'w') as f:
            json.dump(response.to_dict(), f, indent=4)
        print(f"Transcription saved to {OUTPUT_FILE}")

        # Close the file handle and wait a moment before cleanup
        buffer_data.close()
        time.sleep(1)  # Wait for 1 second to ensure file handles are released

        # Clean up the downloaded audio file
        try:
            os.remove(audio_file)
            print("Temporary audio file removed")
        except Exception as e:
            print(f"Note: Could not remove temporary file {audio_file}: {str(e)}")
            print("You may want to delete it manually later.")

if __name__ == '__main__':
    main()