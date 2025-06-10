import json
from datetime import datetime

def convert_to_markdown(json_file, output_file):
    # Read the JSON file
    with open(json_file, 'r') as f:
        data = json.load(f)
    
    # Extract the transcription with speaker diarization
    words = data.get('results', {}).get('channels', [{}])[0].get('alternatives', [{}])[0].get('words', [])
    
    # Get metadata
    duration = data.get('metadata', {}).get('duration', 0)
    created = data.get('metadata', {}).get('created', '')
    
    # Process words into speaker segments
    current_speaker = None
    current_text = []
    speaker_segments = []
    
    for word in words:
        speaker = word.get('speaker', 0)
        text = word.get('word', '')
        
        if current_speaker is None:
            current_speaker = speaker
            
        if speaker != current_speaker:
            # Save the previous segment
            if current_text:
                speaker_segments.append({
                    'speaker': current_speaker,
                    'text': ' '.join(current_text)
                })
            current_speaker = speaker
            current_text = []
            
        current_text.append(text)
    
    # Add the last segment
    if current_text:
        speaker_segments.append({
            'speaker': current_speaker,
            'text': ' '.join(current_text)
        })
    
    # Format the markdown content with speaker segments
    markdown_content = f"""# Audio Transcription

## Metadata
- Duration: {duration:.2f} seconds
- Created: {created}

## Transcription
"""
    
    # Add each speaker segment
    for segment in speaker_segments:
        markdown_content += f"\n**Speaker {segment['speaker']}:** {segment['text']}\n"
    
    # Write to markdown file
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(markdown_content)
    
    print(f"Markdown file created: {output_file}")

if __name__ == '__main__':
    JSON_FILE = 'transcription.json'
    OUTPUT_FILE = 'transcription.md'
    convert_to_markdown(JSON_FILE, OUTPUT_FILE) 