from fastapi import FastAPI, HTTPException
from decouple import config
import uvicorn
import httpx

app = FastAPI()

# Load the Gradio API URL and key from the .env file
gradio_url = config("GRADIO_API_URL")
gradio_api_token = config("GRADIO_API_KEY")

async def make_gradio_request(input_1: str, input_2: str, input_3: str, fn_index: int):
    """
    Make a request to the Gradio API with provided input data and fn_index.

    Args:
        input_1 (str): The first input parameter.
        input_2 (str): The second input parameter.
        input_3 (str): The third input parameter.
        fn_index (int): The fn_index parameter for the Gradio API.

    Returns:
        str: Response from the Gradio API.
    """
    async with httpx.AsyncClient() as client:
        headers = {
            "Authorization": f"Bearer {gradio_api_token}"  # Replace with the appropriate authentication method
        }
        payload = {
            "input_1": input_1,
            "input_2": input_2,
            "input_3": input_3,
            "fn_index": fn_index
        }
        try:
            response = await client.post(f"{gradio_url}/api/predict", json=payload, headers=headers)
            return response.text
        except httpx.RequestError as e:
            raise HTTPException(status_code=500, detail=f"Request to Gradio API failed: {e}")

@app.get("/preset-voice")
async def predict_from_preset_voices(voice_type: str = "random", model_preset: str = "ultrafast", text: str = "Howdy!", fn_index: int = 0):
    """
    Route for predicting text-to-speech from preset voices.

    Args:
        voice_type (str): The type of preset voice to use.
        model_preset (str): The model preset for TTS.
        text (str): The text to be converted to speech.
        fn_index (int): The fn_index parameter for the Gradio API.

    Returns:
        str: Response from the Gradio API.
    """
    return await make_gradio_request(voice_type, text, model_preset, fn_index)

@app.get("/custom-voices")
async def predict_from_custom_voice(path_to_audios: list[str], split_in_chunks: bool = True, text: str = "Howdy!", fn_index: int = 1):
    """
    Route for predicting text-to-speech from custom voices.

    Args:
        path_to_audios (list[str]): List of audio file paths or URLs.
        split_in_chunks (bool): Whether to split audio into chunks.
        text (str): The text to be converted to speech.
        fn_index (int): The fn_index parameter for the Gradio API.

    Returns:
        str: Response from the Gradio API.
    """
    return await make_gradio_request(path_to_audios, split_in_chunks, text, fn_index)

@app.get("/predict-from-one-file")
async def predict_from_live_recording(path_to_audio: str, split_in_chunks: bool = True, text: str = "Howdy!", fn_index: int = 2):
    """
    Route for predicting text-to-speech from a single audio file.

    Args:
        path_to_audio (str): Path to the audio file or URL.
        split_in_chunks (bool): Whether to split audio into chunks.
        text (str): The text to be converted to speech.
        fn_index (int): The fn_index parameter for the Gradio API.

    Returns:
        str: Response from the Gradio API.
    """
    return await make_gradio_request(path_to_audio, split_in_chunks, text, fn_index)



if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
