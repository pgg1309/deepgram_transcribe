import yt_dlp
import os

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
    # Test URL - a short video to test with
    test_url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"  # Rick Astley - Never Gonna Give You Up
    
    print("Testing YouTube audio download...")
    print(f"URL: {test_url}")
    
    audio_file = download_youtube_audio(test_url)
    
    if audio_file and os.path.exists(audio_file):
        print(f"Success! Audio downloaded to: {audio_file}")
        print(f"File size: {os.path.getsize(audio_file) / (1024*1024):.2f} MB")
        
        # Clean up the test file
        os.remove(audio_file)
        print("Test file cleaned up")
    else:
        print("Download failed!")

if __name__ == '__main__':
    main() 