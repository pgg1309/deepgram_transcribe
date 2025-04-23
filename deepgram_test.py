from deepgram import DeepgramClient, PrerecordedOptions
import json

# The API key we created in step 3
DEEPGRAM_API_KEY = '890ddae32d35d288f55bf4f1af373b0bf8cd371a'

# Replace with your file path
PATH_TO_FILE = 'scott_bessent.m4a'
OUTPUT_FILE = 'transcription.json'

def main():
    deepgram = DeepgramClient(DEEPGRAM_API_KEY)

    with open(PATH_TO_FILE, 'rb') as buffer_data:
        payload = { 'buffer': buffer_data }

        options = PrerecordedOptions(
            smart_format=True,
            model="nova-2",
            language="en-US",
            diarize=True  # Enable speaker diarization
        )

        # Use the new recommended method
        response = deepgram.listen.rest.v('1').transcribe_file(payload, options)
        
        # Save response to file
        with open(OUTPUT_FILE, 'w') as f:
            json.dump(response.to_dict(), f, indent=4)
        print(f"Transcription saved to {OUTPUT_FILE}")

if __name__ == '__main__':
    main()