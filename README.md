# AudioSpeakerVerification

This repository contains the code for an **Audio Speaker Verification API** built using FastAPI, SpeechBrain, and Uvicorn. The API allows for the verification and matching of speakers from two different audio files, providing a similarity score and a boolean prediction indicating whether the two audio files are from the same speaker.

## Features

- **Speaker Verification:** Compares two audio files to determine if they are from the same speaker.
- **Pretrained Model:** Utilizes the `speechbrain/spkrec-ecapa-voxceleb` model for accurate speaker recognition.
- **FastAPI:** Provides a simple and efficient API interface.
- **CORS Support:** Enabled CORS middleware to allow cross-origin requests.

## Installation

To set up the API, follow these steps:

1. **Clone the repository:**

   ```bash
   git clone https://github.com/your-username/AudioSpeakerVerification.git
   cd AudioSpeakerVerification

2. **Install dependencies:**

   Make sure you have Python 3.7+ installed, then install the required packages:

   ```bash
   pip install fastapi==0.111.0 speechbrain uvicorn

4. **Launch the API:**

   Start the server with Uvicorn:
   ```bash
   uvicorn main:app --host 0.0.0.0 --port 5000
   The API will be accessible at http://localhost:5000.


