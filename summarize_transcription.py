import os
from openai import OpenAI
import json

# OpenRouter API configuration
OPENROUTER_API_KEY = os.getenv('OPENROUTER_API_KEY')
if not OPENROUTER_API_KEY:
    raise ValueError("Please set the OPENROUTER_API_KEY environment variable")

# Model configuration
MODEL_MAX_CONTEXT = 512000  # Llama 4 Scout free version context length
PROMPT_TOKENS = 200  # Estimated tokens for system prompt and instructions
RESPONSE_BUFFER = 2000  # Increased buffer for larger context model

# Initialize the OpenAI client with OpenRouter
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=OPENROUTER_API_KEY,
)

def count_words(text):
    """Count the number of words in the text."""
    return len(text.split())

def estimate_tokens(text):
    """Estimate the number of tokens in the text."""
    # Rough estimate: 1.5 tokens per word
    return int(len(text.split()) * 1.5)

def read_transcription(file_path):
    """Read the transcription markdown file."""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
        word_count = count_words(content)
        token_estimate = estimate_tokens(content)
        print(f"Transcription contains {word_count} words (estimated {token_estimate} tokens)")
        return content, token_estimate

def calculate_max_tokens(input_tokens):
    """Calculate appropriate max_tokens based on input length and model limits."""
    # Calculate available tokens for response
    available_tokens = MODEL_MAX_CONTEXT - input_tokens - PROMPT_TOKENS
    
    # Ensure we don't exceed the model's context length
    max_response_tokens = min(available_tokens, RESPONSE_BUFFER)
    
    if max_response_tokens < 100:
        raise ValueError(f"Input too long. Estimated {input_tokens} tokens exceeds model's capacity.")
    
    return max_response_tokens

def summarize_transcription(transcription, input_tokens):
    """Summarize the transcription using Llama 4 Scout."""
    max_tokens = calculate_max_tokens(input_tokens)
    print(f"Using max_tokens: {max_tokens}")
    
    prompt = f"""Summarize the key points from the conversation between
      [government official/central banker/top economist/top entrepreneur] and the interviewer.
       Focus on:
        - The main takeaways and insights shared by the interviewee.
        - Any stated or implied policy directions, economic outlooks, or strategic priorities.
        - The implications of the discussion for financial markets, including potential impacts on asset prices such as stocks, bonds, and credit.
        - Any notable risks, opportunities, or signals for investors highlighted in the conversation.

    Write the summary in a clear, concise manner suitable for a professional audience interested in actionable market insights.

    Transcription:
    {transcription}
    """

    response = client.chat.completions.create(
        model="meta-llama/llama-4-scout:free",
        messages=[
            {"role": "system", "content": "You are a financial analyst, PhD economist, CFA with over 20 years of experience, creating concise, factual summaries for investors. Focus on key financial information and business implications."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.4,  # Lower temperature for more factual output
        max_tokens=max_tokens
    )

    return response.choices[0].message.content

def main():
    # File paths
    transcription_file = 'transcription.md'
    summary_file = 'summary.md'

    # Read the transcription
    print("Reading transcription file...")
    transcription, input_tokens = read_transcription(transcription_file)

    # Generate summary
    print("Generating summary...")
    summary = summarize_transcription(transcription, input_tokens)

    # Save summary to file
    with open(summary_file, 'w', encoding='utf-8') as f:
        f.write(f"# Summary\n\n{summary}")
    
    print(f"Summary saved to {summary_file}")

if __name__ == '__main__':
    main() 