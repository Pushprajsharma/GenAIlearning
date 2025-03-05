import tkinter as tk
import speech_recognition as sr
from tkinter import filedialog, Text
import pyttsx3 as tts
from datetime import datetime
import wave

# Supporting Functions

def append_text_to_file(text_to_append):
    try:
        filePath = 'logFile.txt'
        with open(filePath, 'a') as file:
            currentTime = datetime.now()
            file.write(str(currentTime) + " | " + text_to_append + '\n')
    except Exception as e:
        print(f"Error: {e}")

def textToSpeech():
    append_text_to_file("Getting text from text area")
    text = text_area.get("1.0",'end-1c')
    append_text_to_file("Text From text Area : "+text)
    # print(text)
    # What is pyttsx3
    # It is a text-to-speech conversion library in Python. 
    # Unlike alternative libraries, it works offline, and is compatible with both Python 2 and 3.

    try:
        append_text_to_file("Initializing Text to Speech Engine")
        engine = tts.init()
        # other features that are optional to use with the engine
        # 1: Modify rate and volume
        # engine.setProperty('rate', 150)  # Speech speed (default ~200)
        # engine.setProperty('volume', 1.0)  # Volume (0.0 to 1.0)

        # 2 : Change Voice
        # voices = engine.getProperty('voices')
        # for voice in voices:
        #     print(voice, voice.id)
            # engine.setProperty('voice', voice.id)
        # engine.setProperty('voice',voices[1].id)

        engine.say(text)
        append_text_to_file("Text to Speech Converted Successfully")
        # Way to save audio in a file
        audioFileName = 'test.mp3'
        engine.save_to_file(text, audioFileName)
        append_text_to_file("Audio File Saved Successfully")
        engine.runAndWait()
    except Exception as e: 
        append_text_to_file("Error in Text to Speech Conversion :"+str(e))

def speechToTextUsingMicroPhone():
    # SpeechRecognition is a library in python that converts Speech to text by utilizing various
    # APIs provided by Google, IBM, Microsoft Bing, CMU Sphinx
    append_text_to_file("Initializing Speech Recognition engine for Microphone")
    recognizer = sr.Recognizer()

    append_text_to_file("Using Microphone as source")
    with sr.Microphone() as source:
        append_text_to_file("Listening Audio from Microphone")
        audio = recognizer.listen(source)
        try:
            append_text_to_file("Converting Audio to Text")
            text = recognizer.recognize_google(audio)
            text_area.insert(tk.END, text + " ")
            append_text_to_file("Speech to Text Conversion Successful")
        except sr.UnknownValueError:
            append_text_to_file("Could not understand audio")
        except sr.RequestError:
            append_text_to_file("Could not request results")
        except Exception as e:
            append_text_to_file("Exception in creating text from audio: " + str(e))

def speechToTextUsingAudioFile():
    fulltext = ""
    append_text_to_file("Initializing Speech Recognition engine from Audio File")
    filePath = filedialog.askopenfilename(filetypes=[("Audio files", "*.wav")])

    if filePath:
        append_text_to_file("Valid File Found " + filePath)
        recognizer = sr.Recognizer()
        with wave.open(filePath, 'rb') as audio_file:
            append_text_to_file("Recognizing Audio from file")
            frame_rate = audio_file.getframerate()
            chunk_size = frame_rate * 10  # 10 seconds
            audio = sr.AudioFile(filePath)
            with audio as source:
                offset = 0
                while True:
                    audio_data = recognizer.record(source, offset=offset)
                    if not audio_data.frame_data:
                        break
                    try:
                        text = recognizer.recognize_google(audio_data)
                        text_area.insert(tk.END, text + " ")
                    except sr.UnknownValueError:
                        append_text_to_file("Could not understand audio chunk at offset " + str(offset))
                    except sr.RequestError:
                        append_text_to_file("Could not request results for audio chunk at offset " + str(offset))
                    except Exception as e:
                        append_text_to_file("Exception in creating text from audio: " + str(e))
                    offset += 10


def speechToTextMp3():
    file_path = filedialog.askopenfilename(filetypes=[("Audio files", ["*.mp3", "*.wav"])])
    if file_path:
        recognizer = sr.Recognizer()
        with sr.AudioFile(file_path) as source:
            audio = recognizer.record(source)
            try:
                text = recognizer.recognize_google(audio)
                text_area.delete(1.0, tk.END)
                text_area.insert(tk.END, text)
            except sr.UnknownValueError:
                text_area.insert(tk.END, "Could not understand audio")
            except sr.RequestError:
                text_area.insert(tk.END, "Could not request results")


def checkForSource(source):
    append_text_to_file("User has chosen " + source + " as source")
    if source == 'Microphone':
        speechToTextUsingMicroPhone()
    else:
        speechToTextUsingAudioFile()

def uploadTextFile():
    append_text_to_file("User has chosen to upload text file")
    filePath = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
    if filePath:
        append_text_to_file("Valid File Found " + filePath)
        with open(filePath, 'r') as file:
            text = file.read()
            engine = tts.init()
            engine.say(text)
            audioFileName = 'test.mp3'
            engine.save_to_file(text, audioFileName)
            append_text_to_file("Text to Speech Converted Successfully using File")
            engine.runAndWait()

# Initialize the application GUI first
app = tk.Tk()
app.title("Speech to Text / Text to Speech Converter")

# Creating a Frame to hold text Area and buttons
frame = tk.Frame(app)
frame.pack(pady=10, padx=20)

# Creating a Text Area  
text_area = tk.Text(frame, height=10, width=50)
text_area.pack(pady=20)

# creation of Buttons

speechToTextButton = tk.Button(frame, text="Speech to Text", command=lambda: checkForSource('Microphone'))
speechToTextButton.pack(side=tk.LEFT)

speechToTextButton2 = tk.Button(frame, text="Upload Audio File", command=lambda: checkForSource('Audio File'))
speechToTextButton2.pack(side=tk.LEFT)

textToSpeechButton = tk.Button(frame, text="Text To Speech", command=textToSpeech)
textToSpeechButton.pack(side=tk.LEFT, padx=5)

speechToTextButton = tk.Button(frame, text="Upload Text File", command=uploadTextFile)
speechToTextButton.pack(side=tk.LEFT, padx=5)

app.mainloop()