# Security Voice-code Access

This project implements a Security Voice-code Access system using Python, PyQt5, and Qt Designer. The system can be trained on 8 individuals and operates in two modes: Security voice code and Security voice fingerprint.

## Features

- **Mode 1: Security voice code**
  - Access is granted only when a specific pass-code sentence is spoken.
  - Valid passcode sentences:
    - "Open the door"
    - "Unlock middle gate"
    - "Give me access"
  - Customizable passcode sentences without similar words among the three chosen sentences.
- **Mode 2: Security voice fingerprint**
  - Access is granted based on the speaker's voice and the valid passcode sentence.
  - Users can select which of the original 8 users are granted access.
  - Access can be granted to one or more individuals.

## User Interface

The UI includes the following elements:
- Button to start recording the voice-code.
- Spectrogram viewer for the spoken voice-code.
- Summary for analysis results which is the Eculedian distance, therefore less distance is better (it must be less than the threshold):
  - Table showing how much the spoken sentence matches each of the saved passcode sentences.
  - Table showing how much the spoken voice matches each of the 8 saved individuals.
- UI element indicating the algorithm results: "Access gained" or "Access denied".

## Screenshots

1. Mode 1 - Correct passcode sentence (Threshold for the spoken sentence must be less than 11000):
   
   ![image](https://github.com/alimaged10/Voice-Security-Access-System/assets/115377600/089d197a-586b-4da0-99f6-81aa7a8b9db6)

2. Mode 1 - Incorrect passcode sentence (Threshold for the spoken sentence must be less than 11000):
   
   ![image](https://github.com/alimaged10/Voice-Security-Access-System/assets/115377600/16750b58-8b4e-4228-ba59-c6517d60ab33)

3. Mode 2 - Correct passcode sentence with correct speaker (Threshold for the speaking speaker must be less than 8500):
   
   ![image](https://github.com/alimaged10/Voice-Security-Access-System/assets/115377600/28edc5c9-81fb-4612-ab47-383d587deb24)

4. Mode 2 - Correct passcode sentence with incorrect speaker (Threshold for the speaking speaker must be less than 8500):
   Although the (Open the door threshold was met, but the speaker threshold wasn't met, therefore the access is denied)
   ![image](https://github.com/alimaged10/Voice-Security-Access-System/assets/115377600/ca4a6b52-2ae9-4908-90cf-e1d7cb095be0)


## Contributors

- Ali Maged
- Mina Adel
- Mariem Magdy
- Mariam hany

Under the supervision of Dr.Tamer Basha, SBME 2025
