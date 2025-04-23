from deepgram import DeepgramClient, PrerecordedOptions
import json
import os
from pathlib import Path

# The API key we created in step 3
DEEPGRAM_API_KEY = '890ddae32d35d288f55bf4f1af373b0bf8cd371a'

# Configuration
AUDIO_FOLDER = 'audio_files'  # Folder containing audio files
OUTPUT_FOLDER = 'transcriptions'  # Folder for transcriptions

def ensure_folders_exist():
    """Create necessary folders if they don't exist"""
    os.makedirs(AUDIO_FOLDER, exist_ok=True)
    os.makedirs(OUTPUT_FOLDER, exist_ok=True)

def get_audio_files():
    """Get all audio files from the audio folder"""
    audio_extensions = ('.mp3', '.wav', '.m4a', '.ogg', '.flac')
    audio_files = []
    
    for file in os.listdir(AUDIO_FOLDER):
        if file.lower().endswith(audio_extensions):
            audio_files.append(os.path.join(AUDIO_FOLDER, file))
    
    return audio_files

def transcribe_audio(audio_file):
    """Transcribe a single audio file using Deepgram"""
    try:
        # Initialize Deepgram client
        deepgram = DeepgramClient(DEEPGRAM_API_KEY)

        with open(audio_file, 'rb') as buffer_data:
            payload = { 'buffer': buffer_data }

            options = PrerecordedOptions(
                smart_format=True,
                model="nova-2",
                language="en-US",
                diarize=True  # Enable speaker diarization
            )

            print(f"Transcribing {os.path.basename(audio_file)}...")
            # Use the new recommended method
            response = deepgram.listen.rest.v('1').transcribe_file(payload, options)
            
            # Create output filename
            base_name = os.path.splitext(os.path.basename(audio_file))[0]
            output_file = os.path.join(OUTPUT_FOLDER, f"{base_name}_transcription.json")
            
            # Save response to file
            with open(output_file, 'w') as f:
                json.dump(response.to_dict(), f, indent=4)
            print(f"Transcription saved to {output_file}")
            
            return True
    except Exception as e:
        print(f"Error processing {audio_file}: {str(e)}")
        return False

def main():
    # Ensure folders exist
    ensure_folders_exist()
    
    # Get all audio files
    audio_files = get_audio_files()
    
    if not audio_files:
        print(f"No audio files found in {AUDIO_FOLDER} folder.")
        print("Supported formats: .mp3, .wav, .m4a, .ogg, .flac")
        return
    
    print(f"Found {len(audio_files)} audio file(s) to process:")
    for file in audio_files:
        print(f"- {os.path.basename(file)}")
    
    # Process each audio file
    success_count = 0
    for audio_file in audio_files:
        if transcribe_audio(audio_file):
            success_count += 1
    
    print(f"\nProcessing complete!")
    print(f"Successfully transcribed {success_count} out of {len(audio_files)} files.")
    print(f"Transcriptions are saved in the {OUTPUT_FOLDER} folder.")

if __name__ == '__main__':
    main() 