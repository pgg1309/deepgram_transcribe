from moviepy.editor import VideoFileClip
import os
from pathlib import Path

def extract_audio_from_video(video_path, output_format='mp3'):
    """
    Extract audio from a video file and save it as an audio file.
    
    Args:
        video_path (str): Path to the video file
        output_format (str): Format to save the audio (mp3 or wav)
    
    Returns:
        str: Path to the extracted audio file
    """
    # Create output directory if it doesn't exist
    output_dir = 'audio_files'
    os.makedirs(output_dir, exist_ok=True)
    
    # Get the video filename without extension
    video_name = Path(video_path).stem
    
    # Create output path
    output_path = os.path.join(output_dir, f"{video_name}.{output_format}")
    
    try:
        # Load the video file
        video = VideoFileClip(video_path)
        
        # Extract the audio
        audio = video.audio
        
        # Save the audio file
        audio.write_audiofile(output_path)
        
        # Close the video and audio objects
        audio.close()
        video.close()
        
        print(f"Successfully extracted audio to: {output_path}")
        return output_path
        
    except Exception as e:
        print(f"Error extracting audio: {str(e)}")
        return None

def main():
    # Test with main.mp4
    video_file = "main.mp4"
    
    if not os.path.exists(video_file):
        print(f"Error: {video_file} not found in the current directory")
        return
    
    # Extract audio as MP3
    audio_file = extract_audio_from_video(video_file)
    
    if audio_file:
        print("Audio extraction completed successfully!")
    else:
        print("Audio extraction failed.")

if __name__ == "__main__":
    main() 