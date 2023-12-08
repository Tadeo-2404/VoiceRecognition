import speech_recognition as sr
import subprocess
import cv2
import os
from gtts import gTTS

recognizer = sr.Recognizer()
recognizerAudio = sr.Recognizer()
mic = sr.Microphone()
arrCommands = []
exit_flag = True

def record_video():
    fourcc = cv2.VideoWriter_fourcc(*'XVID')  # You can change the codec as needed
    out = cv2.VideoWriter('output.avi', fourcc, 20.0, (640, 480))  # Adjust the parameters as needed
    vid = cv2.VideoCapture(0) 
    while(True):
        ret, frame = vid.read() 
        cv2.imshow('frame', frame) 
        out.write(frame)
        print('Press Q keyword to stop recording')
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    vid.release() 
    cv2.destroyAllWindows() 
    
def record_audio():
    with mic as source:
        print("Speak something:")
        recognizerAudio.adjust_for_ambient_noise(source)
        audioCall = recognizerAudio.listen(source)

        try:
            text = recognizerAudio.recognize_google(audioCall)
            print("You said:", text)

            # Save the recognized text to a file
            with open('recorded_audio_text.txt', 'w') as f:
                f.write(text)

            # Language
            language = 'en'
            tts = gTTS(text=text, lang=language, slow=False)
            tts.save('output_audio.mp3')
            print("Audio recording completed.")
        except sr.UnknownValueError:
            print("Could not understand the audio, try again")
        except sr.RequestError as e:
            print(f"Error: {e}")

def run_command(command: str):
    global exit_flag
    arrCommands.append(command)
    command = command.lower()
    print("I understood:", command)
    #OPEN NOTEPAD
    if "open notepad" in command:
        subprocess.Popen("notepad.exe")
    #CLOSE NOTEPAD
    elif "close notepad" in command:
        subprocess.run(["taskkill", "/F", "/IM", "notepad.exe"])
    #OPEN EDGE BROWSER
    elif "open edge" in command:
        subprocess.Popen(r"C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe")
    #CREATE FILE
    elif "create file" in command:
        with open('text.txt', 'w') as f:
            for element in arrCommands:
                f.write(element + '\n')
    #RECORD VIDEO
    elif "record video" in command:
        record_video()
    #RECORD AUDIO
    elif "record audio" in command:
        record_audio()
    #CLEAR TERMINAL
    elif "clean terminal" in command:
        os.system('cls')
    #exit_flag THE APP
    elif "exit" in command:
        exit_flag = False

def listen_command():
    with mic as source:
        print("I'm all ears:")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

        try:
            text = recognizer.recognize_google(audio)
            run_command(text)
        except sr.UnknownValueError:
            print("Could not understand the audio, try again")
        except sr.RequestError as e:
            print(f"Error: {e}")

while exit:
    listen_command()
