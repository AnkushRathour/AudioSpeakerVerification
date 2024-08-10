import os
import tempfile
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from speechbrain.inference.speaker import SpeakerRecognition
import uvicorn

app = FastAPI(
  title='Audio Speaker Matching API',
  description=(
    'Audio Speaker verification/matching in two different audio files.'
  ),
  version='0.1',
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

# Load the pretrained model for speaker recognition
verification = SpeakerRecognition.from_hparams(
    source="speechbrain/spkrec-ecapa-voxceleb",
    savedir="pretrained_models/spkrec-ecapa-voxceleb"
)

# Function to verify if two audio files are from the same speaker
def verify_speaker(audio_file1, audio_file2):
    # Verify files and get similarity score and prediction
    score, prediction = verification.verify_files(audio_file1, audio_file2)
    return float(score), bool(prediction)

@app.post("/verify-speaker/")
async def verify_speaker_endpoint(file1: UploadFile = File(...), file2: UploadFile = File(...)):
    file_formats = ["audio/m4a", "audio/mpeg", "audio/mp3", "audio/wav"]
    if file1.content_type not in file_formats or file2.content_type not in file_formats:
        raise HTTPException(
            status_code=415,
            detail=f"Unsupported File Type. Supported file type {file_formats}."
        )

    try:
        # Get the file extensions
        suffix1 = file1.filename.split('.')[-1]
        suffix2 = file1.filename.split('.')[-1]

        with tempfile.NamedTemporaryFile(delete=False, suffix=f'.{suffix1}') as tmp_file1, \
          tempfile.NamedTemporaryFile(delete=False, suffix=f'.{suffix2}') as tmp_file2:
            tmp_file1.write(await file1.read())
            tmp_file2.write(await file2.read())
            audio_file1 = tmp_file1.name
            audio_file2 = tmp_file2.name

        score, prediction = verify_speaker(audio_file1, audio_file2)

        # Clean up temporary files
        os.remove(audio_file1.split('/')[2])
        os.remove(audio_file2.split('/')[2])

        context = {
            "similarity_score": score,
            "same_speaker": prediction
        }
        return JSONResponse(content=context)
    except Exception as e:
      context = {
          "error": str(e),
          "similarity_score": None,
          "same_speaker": None,
          "detail": "An error occurred while verifying the speaker."
      }
      return JSONResponse(content=context)


if __name__ == "__main__":
    uvicorn.run(app, host='0.0.0.0', port=5000)
