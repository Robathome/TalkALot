#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun 13 15:53:18 2024

@author: rob
"""

import tkinter as tk  
from tkinter import messagebox  
import speech_recognition as sr  
from pydub import AudioSegment  
from pydub.playback import play  
from pocketsphinx import LiveSpeech, get_model_path

class SpeechTherapyApp:
    def __init__(self, root):
        self.root = root  
        self.root.title("Speech Therapy App")

        self.label = tk.Label(root, text="Select a word to practice:", font=("Arial", 16))
        self.label.pack(pady=10)

        self.word_list = ["apple", "banana", "cherry"]
        self.word_var = tk.StringVar(value=self.word_list[0])

        self.word_menu = tk.OptionMenu(root, self.word_var, *self.word_list)
        self.word_menu.pack(pady=10)

        self.play_button = tk.Button(root, text="Play Word", command=self.play_word)
        self.play_button.pack(pady=10)

        self.record_button = tk.Button(root, text="Record Pronunciation", command=self.record_pronunciation)
        self.record_button.pack(pady=10)

        self.feedback_label = tk.Label(root, text="", font=("Arial", 14))
        self.feedback_label.pack(pady=10)

        self.grapheme_dict = {
            "apple": ["a", "p", "p", "l", "e"],
            "banana": ["b", "a", "n", "a", "n", "a"],
            "cherry": ["ch", "e", "rr", "y"]
        }

    def play_word(self):
        word = self.word_var.get()
        audio = AudioSegment.from_file(f"{word}.mp3")
        play(audio)

    def record_pronunciation(self):
        recognizer = sr.Recognizer()
        with sr.Microphone() as source:
            self.feedback_label.config(text="Recording...")
            audio_data = recognizer.listen(source)
            self.feedback_label.config(text="Processing...")

            try:
                # Save the audio data to a file  
                with open("temp_audio.wav", "wb") as f:
                    f.write(audio_data.get_wav_data())

                # Use PocketSphinx to recognize the speech  
                model_path = get_model_path()
                speech = LiveSpeech(
                    audio_file='temp_audio.wav',
                    hmm=model_path + '/en-us',
                    lm=model_path + '/en-us.lm.bin',
                    dic=model_path + '/cmudict-en-us.dict'
                )

                for phrase in speech:
                    self.provide_feedback(str(phrase))

            except Exception as e:
                messagebox.showerror("Error", f"Could not process audio: {e}")

    def provide_feedback(self, transcript):
        word = self.word_var.get()
        expected_graphemes = self.grapheme_dict[word]
        feedback = f"You said: {transcript}\n"

        # Here you would compare the phonemes from the transcript to the expected phonemes  
        # For simplicity, we are just displaying the graphemes

        feedback += "Expected graphemes:\n" + " ".join(expected_graphemes)
        self.feedback_label.config(text=feedback)

if __name__ == "__main__":
    root = tk.Tk()
    app = SpeechTherapyApp(root)
    root.mainloop() 
