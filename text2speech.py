from gradio_client import Client

def text_to_speech(input_file_path, output_file_path="output_audio.wav", voice_name=None, speed=1.0):
    """Convert text from a file to speech using Kokoro-TTS-Zero
    
    Args:
        input_file_path (str): Path to the input text file
        output_file_path (str): Path to save the output audio file
        voice_name (str, optional): Name of the voice to use
        speed (float, optional): Speech speed multiplier
    
    Returns:
        tuple: (audio_path, metrics, performance_summary)
    """
    try:
        # Read text from file
        with open(input_file_path, 'r', encoding='utf-8') as file:
            text_content = file.read().strip()
        
        if not text_content:
            raise ValueError("Input file is empty")
        
        # Initialize Kokoro-TTS-Zero client
        client = Client("Remsky/Kokoro-TTS-Zero")
        
        # Generate speech
        result = client.predict(
            text=text_content,
            voice_names=voice_name,
            speed=speed,
            api_name="/generate_speech_from_ui"
        )
        
        # Unpack results
        audio_path, metrics, performance = result
        
        print(f"Audio generated successfully: {audio_path}")
        print(f"Performance summary: {performance}")
        
        return result
        
    except FileNotFoundError:
        print(f"Error: Input file '{input_file_path}' not found")
        return None
    except Exception as e:
        print(f"Error during text-to-speech conversion: {str(e)}")
        return None

# Example usage
if __name__ == "__main__":
    # Example: Convert a text file to speech
    # Convert text file to speech using Kokoro-TTS-Zero
    # Input: ASAP paper text file
    # Voice: af_nova (default voice)
    # Speed: Normal (1.0x)
    '''result = text_to_speech(
        input_file_path="C:\\Users\\LuisEdwardVeloPoma\\Downloads\\ASAP Aligning Simulation and Real-W.txt",
        voice_name="af_nova",  # Use default voice
        speed=1.0        # Normal speed
    '''
