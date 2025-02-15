# Import Libraries
import re
import nltk
import pandas as pd
import pygame
from pygame import mixer
import os
import string
import random

import speech_recognition as sr
import nltk
from nltk.metrics import edit_distance
from nltk.tokenize import word_tokenize
from moviepy.editor import VideoFileClip
import pygame
import time
import tkinter as tk
from tkinter import messagebox
import random
import pyttsx3
import speech_recognition as sr
from tkinter import ttk

import sqlite3
from tkinter import *
from tkinter import ttk
import tkinter.messagebox as tkMessageBox
import re
from difflib import SequenceMatcher
from tkinter import messagebox
from PIL import Image
def preprocess_text(text):
    # Remove all non-alphabetic characters and convert text to lowercase
    cleaned_text = re.sub(r'[^a-zA-Z\s]', '', text)
    return cleaned_text.lower()

def calculate_similarity(text1, text2):
    # Calculate similarity using SequenceMatcher
    similarity = SequenceMatcher(None, text1, text2).ratio()
    return similarity

def database():
    global conn, cursor
    conn = sqlite3.connect("data.db")
    cursor = conn.cursor()
    q1 = "Create table if not exists user (id integer primary key AUTOINCREMENT,email varchar(150) unique,password TEXT, name TEXT,phone_no TEXT)"
    cursor.execute(q1)
    q1 = "Create table if not exists grade (id integer primary key,letter TEXT, words TEXT,sentense TEXT)"
    cursor.execute(q1)

def login():
    root = Tk()
    em=StringVar(root)
    passwrd=StringVar(root)
    root.title("Phonetics App")
    root.geometry("780x450")
    root.config(bg="#343434")
    def log_in():
        database()
        try:
            e = em.get()
            p = passwrd.get()
            cursor.execute(f'SELECT * FROM user WHERE email = ? AND password = ?', (e, p))
            data=cursor.fetchone()

            if data:
                tkMessageBox.showinfo("Phonetics App","Logged In Successfully !!!")
                root.destroy()
                f = open("cred.txt","w")
                f.write(str(data[0]))
                f.close()
                try:
                    database()
                    cursor.execute(f"INSERT INTO grade(id,letter,words,sentense) VALUES({data[0]},'-','-','-')")
                    conn.commit()
                    conn.close()
                except:
                    pass
                mainwindow()
            else:
                tkMessageBox.showinfo("Phonetics App","Failed To Login !!!")
                em.set("")
                passwrd.set("")
        except Exception as e:
            tkMessageBox.showinfo("Phonetics App",e)
            
    h1 = Label(root, text="-- LOGIN --",fg="#DCB86F",bg="#343434",font=("",24,"bold"))
    h1.place(x=300,y=15)
    h2 = Label(root, text="Email: ",fg="#DCB86F",bg="#343434",font=("",20,"bold"))
    h2.place(x=114,y=120)
    h3 = Label(root, text="Password: ",fg="#DCB86F",bg="#343434",font=("",20,"bold"))
    h3.place(x=60,y=205)
    e1 = Entry(root,textvariable=em,bg="#DCB86F",fg="#343434",font=("",20),width=30)
    e1.place(x=250,y=120)
    e2 = Entry(root,textvariable=passwrd,bg="#DCB86F",fg="#343434",font=("",20),width=30,show='*')
    e2.place(x=250,y=205)
    b1 = Button(root, text="Register",bg="#DCB86F",fg="#343434",font=("",20,"bold"),bd=2,relief="solid",width=18,command=signup)
    b1.place(x=60,y=290)
    b2 = Button(root, text="LOGIN",bg="#DCB86F",fg="#343434",font=("",20,"bold"),bd=2,relief="solid",width=18,command=log_in)
    b2.place(x=390,y=290)
    root.mainloop()

def signup():
    global nme,passwrd,em,phone
    root2 = Tk()
    nme=StringVar(root2)
    passwrd=StringVar(root2)
    em = StringVar(root2)
    phone = StringVar(root2)
    branch = StringVar(root2)

    root2.title("Phonetics App")
    root2.geometry("780x480")
    root2.config(bg="#343434")
    def reg():
   
        global nme,passwrd,em,phone
        database()
        try:
            cursor.execute(f"INSERT INTO user(name,password,email,phone_no) VALUES('{nme.get()}','{passwrd.get()}','{em.get()}','{phone.get()}')")
            conn.commit()
            conn.close()
            tkMessageBox.showinfo("Phonetics App","Registered Successfully !!!")
            root2.destroy()
            login()
        except Exception as e:
            tkMessageBox.showinfo("Phonetics App",e)
    def login2():
            root2.destroy()
            login()        
    h1 = Label(root2, text="-- REGISTER --",fg="#DCB86F",bg="#343434",font=("",24,"bold"))
    h1.place(x=280,y=15)
    h2 = Label(root2, text="Name: ",fg="#DCB86F",bg="#343434",font=("",20,"bold"))
    h2.place(x=60,y=120)
    h3 = Label(root2, text="Password: ",fg="#DCB86F",bg="#343434",font=("",20,"bold"))
    h3.place(x=60,y=180)
    e1 = Entry(root2,textvariable=nme,bg="#DCB86F",fg="#343434",font=("",20),width=30)
    e1.place(x=250,y=120)
    e2 = Entry(root2,textvariable=passwrd,bg="#DCB86F",fg="#343434",font=("",20),width=30)
    e2.place(x=250,y=180)
    h4 = Label(root2, text="Email: ",fg="#DCB86F",bg="#343434",font=("",20,"bold"))
    h4.place(x=60,y=240)
    h5 = Label(root2, text="Phone No.: ",fg="#DCB86F",bg="#343434",font=("",20,"bold"))
    h5.place(x=60,y=300)
    e4 = Entry(root2,textvariable=em,bg="#DCB86F",fg="#343434",font=("",20),width=30)
    e4.place(x=250,y=240)
    e5 = Entry(root2,textvariable=phone,bg="#DCB86F",fg="#343434",font=("",20),width=30)
    e5.place(x=250,y=300)


    b1 = Button(root2, text="Register",font=("",20,"bold"),bg="#DCB86F",fg="#343434",bd=2,relief="solid",width=18,command=reg)
    b1.place(x=60,y=400)
    b2 = Button(root2, text="Back To Login",bg="#DCB86F",fg="#343434",font=("",20,"bold"),bd=2,relief="solid",width=18,command=login2)
    b2.place(x=390,y=400)
    root2.mainloop()


def mainwindow():
    userid = int(open("cred.txt","r").read())
    database()
    cursor.execute(f'SELECT * FROM grade WHERE id = {userid}')
    data=cursor.fetchone()
    avg = 0
    for i in data[1::]:
        if "-" not in data:
            avg+=float(i)
    avg /= 3
    if avg>0:
        if avg<=3 :
            tkMessageBox.showinfo("Phonetics App","Most suitable level for you is Letters")
        elif avg>3 and avg<=7.5:
            tkMessageBox.showinfo("Phonetics App","Most suitable level for you is Words")
        else:
            tkMessageBox.showinfo("Phonetics App","Most suitable level for you is sentences")
            
            
    sentences = [
        "The sun sets in the west.",
        "Cats are known for their agility.",
        "Learning a new language is a rewarding experience.",
        "Coffee is a popular beverage around the world.",
        "The internet has transformed the way we communicate.",
        "Nature is full of wonders and beauty.",
        "Music has the power to evoke strong emotions.",
        "Coding is a valuable skill in today's technology-driven world.",
        "Books open the door to new worlds and perspectives.",
        "The moonlight reflected on the calm lake.",
        "Health is wealth.",
        "Kindness costs nothing but means everything.",
        "Laughter is the best medicine.",
        "The Great Wall of China is a marvel of engineering.",
        "Hiking in the mountains is a great way to connect with nature.",
        "The diversity of cultures makes the world rich and vibrant.",
        "Hard work and perseverance lead to success.",
        "Art allows us to express our inner thoughts and feelings.",
        "Einstein's theory of relativity revolutionized physics.",
        "The oceans are home to a vast array of fascinating creatures.",
        "The Mona Lisa is one of the most famous paintings in the world.",
        "An apple a day keeps the doctor away.",
        "The power of positive thinking can change your life.",
        "Innovation drives progress in technology and science.",
        "Elephants are highly intelligent and social animals.",
        "The sound of waves crashing on the shore is soothing.",
        "Travel broadens the mind.",
        "Dance is a form of self-expression and creativity.",
        "Chocolate is a delightful treat loved by many.",
        "A smile is contagious.",
        "The Silk Road was a historic trade route connecting East and West.",
        "The pen is mightier than the sword.",
        "The Eiffel Tower is an iconic symbol of Paris.",
        "Mount Everest is the highest peak in the world.",
        "The concept of time is a fascinating aspect of human perception.",
        "Friendship is a treasure that grows with time.",
        "Birds of a feather flock together.",
        "The invention of the wheel revolutionized transportation.",
        "A healthy diet is essential for overall well-being.",
        "Sunflowers follow the movement of the sun throughout the day.",
        "The butterfly undergoes a remarkable transformation during its life cycle.",
        "The Northern Lights are a breathtaking natural phenomenon.",
        "Happiness is a choice.",
        "Shakespeare's plays continue to be performed and admired worldwide.",
        "The Great Barrier Reef is a wonder of the underwater world.",
        "The human brain is a complex and remarkable organ.",
        "Yoga promotes physical and mental well-being.",
        "The Declaration of Independence laid the foundation for a new nation.",
        "Rainbows are a beautiful display of color in the sky.",
        "A stitch in time saves nine.",
        "The space race led to significant advancements in technology.",
        "Sunsets are a reminder of the beauty in endings.",
        "Communication is key in building strong relationships.",
        "The Sahara Desert is the largest hot desert in the world.",
        "The concept of justice is fundamental to a fair society.",
        "Ice cream is a favorite treat on hot summer days.",
        "The Wright brothers pioneered human flight with the first airplane.",
        "The Internet of Things is transforming the way we live and work.",
        "Cherry blossoms are a symbol of beauty and transience in Japanese culture.",
        "Soccer is the most popular sport in the world.",
        "The universe is vast and mysterious.",
        "The printing press revolutionized the spread of information.",
        "Gratitude is the key to a happy life.",
        "Tigers are majestic creatures that inspire awe.",
        "The Golden Gate Bridge is an iconic landmark in San Francisco.",
        "Meditation can bring inner peace and mindfulness.",
        "The human heart beats an average of 100,000 times per day.",
        "The concept of democracy has evolved over centuries.",
        "Rainforests are vital for the health of our planet.",
        "The invention of the telephone changed the way we communicate over long distances.",
        "Astronomy explores the wonders of the cosmos.",
        "Cultural diversity enriches societies and promotes understanding.",
        "The pyramids of Egypt are a testament to ancient architectural prowess.",
        "Lifelong learning is the key to personal growth.",
        "The sound of rain tapping on the window is a soothing lullaby.",
        "The four seasons bring variety and beauty to the natural world.",
        "Sailing allows for a unique and peaceful connection with the sea.",
        "Curiosity is the driving force behind scientific discovery.",
        "The Amazon rainforest is home to an incredible array of plant and animal species.",
        "The concept of karma suggests that our actions have consequences.",
        "Chess is a game of strategy and skill.",
        "The Great Depression had a profound impact on the global economy.",
        "Wine is often associated with celebration and relaxation.",
        "The concept of time travel has captured the imagination of many.",
        "The Taj Mahal is a magnificent example of Mughal architecture.",
        "Rivers have played a crucial role in the development of human civilizations.",
        "The smell of fresh-baked bread is irresistible.",
        "The concept of beauty is subjective and varies across cultures.",
        "The piano is a versatile and expressive musical instrument.",
        "The Internet provides access to a vast repository of information.",
        "Bees play a crucial role in pollination and ecosystem health.",
        "The concept of fate has been explored in literature and philosophy.",
        "The Berlin Wall once divided East and West Berlin.",
        "Cooking is a creative and enjoyable form of self-expression.",
        "The concept of artificial intelligence is reshaping the future of technology.",
        "The Colosseum in Rome is a symbol of ancient Roman engineering.",
        "The smell of fresh flowers can uplift the spirits.",
        "Human rights are fundamental to a just and equitable society.",
        "The concept of balance is important in maintaining a healthy lifestyle.",
        "The laughter of children is a source of pure joy.",
        "The principles of physics govern the behavior of the universe.",
        "The Hubble Space Telescope has provided stunning images of distant galaxies.",
        "The concept of love is a powerful and universal force.",
        "Bicycling is an eco-friendly and healthy mode of transportation.",
        "The Inca Trail offers a breathtaking journey to the ancient city of Machu Picchu.",
        "The concept of mindfulness encourages living in the present moment.",
        "The smell of rain on dry earth is called petrichor.",
        "The concept of self-fulfilling prophecy explores the power of belief.",
        "The Louvre Museum in Paris houses an extensive collection of art.",
        "The concept of yin and yang represents balance and harmony in Chinese philosophy.",
        "The sound of waves crashing on the shore is a natural lullaby.",
        "The concept of empathy fosters understanding and compassion.",
        "The Grand Canyon is a stunning example of geological wonders.",
        "The concept of renewable energy is crucial for a sustainable future.",
        "The laughter of a baby is infectious.",
        "The concept of cultural appropriation sparks important conversations about respect.",
        "The Mona Lisa's enigmatic smile continues to captivate art enthusiasts.",
        "The concept of resilience explores the ability to bounce back from adversity.",
        "The Milky Way is a vast galaxy that contains our solar system.",
        "The concept of infinity is mind-boggling and fascinating.",
        "The aroma of freshly brewed coffee is invigorating.",
        "The concept of manifest destiny shaped the expansion of the United States.",
        "The Aurora Borealis is a breathtaking display of lights in the northern hemisphere.",
        "The concept of serendipity celebrates unexpected and fortunate discoveries.",
        "The sound of birdsong in the morning is a natural alarm clock.",
        "The concept of entropy is central to the laws of thermodynamics.",
        "The Great Wall of China is a testament to ancient defensive architecture.",
        "The concept of biodiversity highlights the importance of preserving ecosystems.",
        "The smell of a new book is a delight for bibliophiles.",
        "The concept of cognitive dissonance explores the discomfort of conflicting beliefs.",
        "The Great Sphinx of Giza is an iconic symbol of ancient Egypt.",
        "The concept of supply and demand is fundamental to economics.",
        "The sound of a crackling fireplace is cozy and comforting.",
        "The concept of justice aims to ensure fairness and equality in society.",
        "The Parthenon in Athens is a majestic temple dedicated to the goddess Athena.",
        "The concept of universal gravitation was formulated by Sir Isaac Newton.",
        "The sound of rain tapping on the window is a soothing lullaby.",
        "The concept of beauty is subjective and varies across cultures.",
        "The piano is a versatile and expressive musical instrument.",
        "The Internet provides access to a vast repository of information.",
        "Bees play a crucial role in pollination and ecosystem health.",
        "The concept of fate has been explored in literature and philosophy.",
        "The Berlin Wall once divided East and West Berlin.",
        "Cooking is a creative and enjoyable form of self-expression.",
        "The concept of artificial intelligence is reshaping the future of technology.",
        "The Colosseum in Rome is a symbol of ancient Roman engineering.",
        "The smell of fresh flowers can uplift the spirits.",
        "Human rights are fundamental to a just and equitable society.",
        "The concept of balance is important in maintaining a healthy lifestyle.",
        "The laughter of children is a source of pure joy.",
        "The principles of physics govern the behavior of the universe.",
        "The Hubble Space Telescope has provided stunning images of distant galaxies.",
        "The concept of love is a powerful and universal force.",
        "Bicycling is an eco-friendly and healthy mode of transportation.",
        "The Inca Trail offers a breathtaking journey to the ancient city of Machu Picchu.",
        "The concept of mindfulness encourages living in the present moment.",
        "The smell of rain on dry earth is called petrichor.",
        "The concept of self-fulfilling prophecy explores the power of belief.",
        "The Louvre Museum in Paris houses an extensive collection of art.",
        "The concept of yin and yang represents balance and harmony in Chinese philosophy.",
        "The sound of waves crashing on the shore is a natural lullaby.",
        "The concept of empathy fosters understanding and compassion.",
        "The Grand Canyon is a stunning example of geological wonders.",
        "The concept of renewable energy is crucial for a sustainable future.",
        "The laughter of a baby is infectious.",
        "The concept of cultural appropriation sparks important conversations about respect.",
        "The Mona Lisa's enigmatic smile continues to captivate art enthusiasts.",
        "The concept of resilience explores the ability to bounce back from adversity.",
        "The Milky Way is a vast galaxy that contains our solar system.",
        "The concept of infinity is mind-boggling and fascinating.",
        "The aroma of freshly brewed coffee is invigorating.",
        "The concept of manifest destiny shaped the expansion of the United States.",
        "The Aurora Borealis is a breathtaking display of lights in the northern hemisphere.",
        "The concept of serendipity celebrates unexpected and fortunate discoveries.",
        "The sound of birdsong in the morning is a natural alarm clock.",
        "The concept of entropy is central to the laws of thermodynamics.",
        "The Great Wall of China is a testament to ancient defensive architecture.",
        "The concept of biodiversity highlights the importance of preserving ecosystems.",
        "The smell of a new book is a delight for bibliophiles.",
        "The concept of cognitive dissonance explores the discomfort of conflicting beliefs.",
        "The Great Sphinx of Giza is an iconic symbol of ancient Egypt.",
        "The concept of supply and demand is fundamental to economics.",
        "The sound of a crackling fireplace is cozy and comforting.",
        "The concept of justice aims to ensure fairness and equality in society.",
        "The Parthenon in Athens is a majestic temple dedicated to the goddess Athena.",
        "The concept of universal gravitation was formulated by Sir Isaac Newton.",
        "The sound of rain tapping on the window is a soothing lullaby.",
        "The concept of beauty is subjective and varies across cultures.",
        "The piano is a versatile and expressive musical instrument.",
        "The Internet provides access to a vast repository of information.",
        "Bees play a crucial role in pollination and ecosystem health.",
        "The concept of fate has been explored in literature and philosophy.",
        "The Berlin Wall once divided East and West Berlin.",
        "Cooking is a creative and enjoyable form of self-expression.",
        "The concept of artificial intelligence is reshaping the future of technology.",
        "The Colosseum in Rome is a symbol of ancient Roman engineering.",
        "The smell of fresh flowers can uplift the spirits.",
        "Human rights are fundamental to a just and equitable society.",
        "The concept of balance is important in maintaining a healthy lifestyle.",
        "The laughter of children is a source of pure joy.",
        "The principles of physics govern the behavior of the universe.",
        "The Hubble Space Telescope has provided stunning images of distant galaxies.",
        "The concept of love is a powerful and universal force.",
        "Bicycling is an eco-friendly and healthy mode of transportation.",
        "The Inca Trail offers a breathtaking journey to the ancient city of Machu Picchu.",
        "The concept of mindfulness encourages living in the present moment.",
        "The smell of rain on dry earth is called petrichor.",
        "The concept of self-fulfilling prophecy explores the power of belief.",
        "The Louvre Museum in Paris houses an extensive collection of art.",
        "The concept of yin and yang represents balance and harmony in Chinese philosophy.",
        "The sound of waves crashing on the shore is a natural lullaby.",
        "The concept of empathy fosters understanding and compassion.",
        "The Grand Canyon is a stunning example of geological wonders.",
        "The concept of renewable energy is crucial for a sustainable future.",
        "The laughter of a baby is infectious.",
        "The concept of cultural appropriation sparks important conversations about respect.",
        "The Mona Lisa's enigmatic smile continues to captivate art enthusiasts.",
        "The concept of resilience explores the ability to bounce back from adversity.",
        "The Milky Way is a vast galaxy that contains our solar system.",
        "The concept of infinity is mind-boggling and fascinating.",
        "The aroma of freshly brewed coffee is invigorating.",
        "The concept of manifest destiny shaped the expansion of the United States.",
        "The Aurora Borealis is a breathtaking display of lights in the northern hemisphere.",
        "The concept of serendipity celebrates unexpected and fortunate discoveries.",
        "The sound of birdsong in the morning is a natural alarm clock.",
        "The concept of entropy is central to the laws of thermodynamics.",
        "The Great Wall of China is a testament to ancient defensive architecture.",
        "The concept of biodiversity highlights the importance of preserving ecosystems.",
        "The smell of a new book is a delight for bibliophiles.",
        "The concept of cognitive dissonance explores the discomfort of conflicting beliefs.",
        "The Great Sphinx of Giza is an iconic symbol of ancient Egypt.",
        "The concept of supply and demand is fundamental to economics.",
        "The sound of a crackling fireplace is cozy and comforting.",
        "The concept of justice aims to ensure fairness and equality in society.",
        "The Parthenon in Athens is a majestic temple dedicated to the goddess Athena.",
        "The concept of universal gravitation was formulated by Sir Isaac Newton."
    ]

    class SentencePhoneticsGame:
        def __init__(self, master):
            self.master = master
            self.master.title("Phonetics Transcription Game")
            self.master.geometry("800x400")
            self.master.configure(bg="#ebeef4")

            self.score = 0
            self.tries = 0

            style = ttk.Style()
            style.configure("TLabel", background="#ebeef4")
            style.configure("TButton", background="#f9e7b4", font=("Arial", 12))
            style.configure("TEntry", background="#f9e784", font=("Arial", 12))

            self.title_label = ttk.Label(self.master, text="Sentence Phonetics Game", font=("Arial", 20), style="TLabel")
            self.title_label.pack(pady=20)

            self.score_label = ttk.Label(self.master, text=f"Score: {self.score}", font=("Arial", 14), style="TLabel")
            self.score_label.pack(pady=10)

            self.sentence_label = ttk.Label(self.master, text="", font=("Arial", 14), style="TLabel")
            self.sentence_label.pack(pady=10)

            self.transcription_entry = ttk.Entry(self.master, font=("Arial", 12), width=40)
            self.transcription_entry.pack(pady=10)

            self.check_button = ttk.Button(self.master, text="Check", command=self.check_transcription, style="TButton", width=40)
            self.check_button.pack(pady=10)

            self.speak_button = ttk.Button(self.master, text="Listen Correct Pronunciation", command=self.speak_sentence, style="TButton", width=40)
            self.speak_button.pack(pady=10)

            self.listen_button = ttk.Button(self.master, text="Speak Sentence and Transcribe", command=self.listen_and_transcribe, style="TButton", width=40)
            self.listen_button.pack(pady=10)

            self.engine = pyttsx3.init()

            self.next_sentence()

        def get_random_sentence(self):
            # Implement logic to fetch a random sentence from the database
            # For simplicity, using a hardcoded list of sentences here.
            return random.choice(sentences)

        def transcribe_sentence(self, sentence):
            # Implement phonetic transcription logic
            # For simplicity, returning the same sentence.
            return sentence

        def speak_sentence(self):
            sentence = self.sentence_label.cget("text")[10:]
            self.engine.say(sentence)
            self.engine.runAndWait()

        def listen_and_transcribe(self):
            recognizer = sr.Recognizer()
            with sr.Microphone() as source:
                self.engine.say("Listening...")
                self.engine.runAndWait()
                audio_input = recognizer.listen(source)
                print(audio_input)
            try:
                user_transcription = recognizer.recognize_google(audio_input)
                self.transcription_entry.delete(0, tk.END)
                self.transcription_entry.insert(tk.END, user_transcription)
            except sr.UnknownValueError:
                messagebox.showwarning("Speech Recognition", "Sorry, could not understand audio.")
            except sr.RequestError as e:
                messagebox.showerror("Speech Recognition", f"Error with the speech recognition service: {e}")

        def next_sentence(self):
            self.transcription_entry.delete(0, tk.END)
            sentence = self.get_random_sentence()
            self.sentence_label.config(text=f"Sentence: {sentence}")
            self.score_label.config(text=f"Score: {self.score}")


        def check_transcription(self):
                user_transcription = self.transcription_entry.get()
                current_sentence = self.sentence_label.cget("text")[10:]  # Extracting the sentence from the label text

                # Preprocess the user's transcription and correct transcription
                user_transcription_cleaned = preprocess_text(user_transcription)
                current_sentence_cleaned = preprocess_text(current_sentence)

                # Calculate similarity
                similarity = calculate_similarity(user_transcription_cleaned, current_sentence_cleaned)
                
                self.tries += 1

                # Define a similarity threshold (e.g., 80%)
                threshold = 0.8

                if similarity >= threshold:
                    messagebox.showinfo("Correct!", f"Well done! Similarity: {similarity*100:.2f}%")
                    self.score += 1
                else:
                    messagebox.showerror("Incorrect", f"The correct transcription is: {current_sentence}\nSimilarity: {similarity*100:.2f}%")

                database()
                if self.tries<10:
                    x = self.score/self.tries
                else:
                    x = (self.score/self.tries)*10
                if x>=9 and self.tries>=10:
                    tkMessageBox.showinfo("Phonetics App","You are going great job in this level")
                cursor.execute(f"UPDATE grade set sentense='{x}' where id={userid}")
                conn.commit()
                conn.close()
                self.next_sentence()

    image_dir = 'Image'
    audio_dir = 'Audio'
    video_dir = './Video//'



    def play_video(video_path, speed):
        pygame.display.update()
        clip = VideoFileClip(video_path)
        clip = clip.speedx(speed)
        clip = clip.resize((640, 580)) 
        clip.preview()
        pygame.display.update()
        

    def play_word_videos(folder_path, word):
        pygame.display.update()

        if speed<1:
            sp=speed/2+0.15
        else:
            sp = speed/2
        time.sleep(2)
        for char in word:
            if char.isalpha():
                char_lower = char.lower()
                if char.isupper():
                    video_path = f"{char}.mp4"
                else:
                    video_path = f"_{char_lower}.mp4"

                try:
                    play_video(folder_path + video_path, sp)
                    
                except FileNotFoundError:
                    print(f"Video for '{char}' not found.")
        pygame.display.update()

    def calculate_token_scores(correct_word, user_input):
        # Tokenize the correct word and user input
        correct_tokens = word_tokenize(correct_word)
        user_tokens = word_tokenize(user_input)
        
        # Initialize a dictionary to store token scores
        token_scores = {}
        
        # Calculate Levenshtein distance for each token
        for correct_token in correct_tokens:
            min_distance = float('inf')
            for user_token in user_tokens:
                distance = edit_distance(correct_token, user_token)
                min_distance = min(min_distance, distance)
            token_scores[correct_token] = 1 - (min_distance / max(len(correct_token), len(user_token)))
        
        return token_scores

    def calculate_overall_score(token_scores):
        # Calculate the overall score as the average of token scores
        overall_score = sum(token_scores.values()) / len(token_scores)
        return overall_score

    # Open Word List
    with open("word_list.txt", "r") as f:
        word_list = [word.replace('\n', '') for word in f.readlines()]

    # Substitute Symbols with Spaces
    word_list = [re.sub('[-.]', ' ', word) for word in word_list]
    # Remove Words with Spaces
    word_list = list(filter(lambda x: ' ' not in x, word_list))
    # Change to Lower Cases
    word_list = [word.lower() for word in word_list]
    # Keep the Words with 3 or 4 Characters
    word_list = list(filter(lambda x: len(x) in [1, 3, 4], word_list))

    # List of Part-of-Speech
    pos_list = [nltk.pos_tag([word])[0][1] for word in word_list]
    # List of Word Length
    len_list = [len(word) for word in word_list]
    # Data Frame
    word_df = pd.DataFrame({'Word': word_list, 'POS': pos_list, 'Len': len_list})
    # Keep CD / JJ / NN / VB
    word_df = word_df[word_df['POS'].isin(['CD', 'JJ', 'NN', 'VB'])]

    # Game Init
    pygame.init()
    win = pygame.display.set_mode((640, 580))
    pygame.display.set_caption("Voice Virtuoso")

    mixer.init()

    pygame.font.init()
    font_1 = pygame.font.SysFont('impact', 55)
    font_2 = pygame.font.SysFont('Arial', 25)
    font_3 = pygame.font.SysFont('roboto', 30)
    font_4 = pygame.font.SysFont('Arial', 20)
    font_5 = pygame.font.SysFont('impact', 25)
    font_6 = pygame.font.SysFont('impact', 120)
    font_7 = pygame.font.SysFont('impact', 90)

    clock = pygame.time.Clock()
    pygame.time.set_timer(pygame.USEREVENT, 1000)

    #############
    # Main Page #
    #############

    page = 0
    flag = False
    # Background
    win.fill((208, 83, 83))  # title
    pygame.draw.rect(win, (229, 143, 101), (0, 200, 640, 110))  # word length
    pygame.draw.rect(win, (249, 231, 132), (0, 310, 640, 110))  # time limit
    pygame.draw.rect(win, (249, 231, 180), (0, 420, 640, 110))  # time limit
    pygame.draw.rect(win, (235, 238, 244), (0, 530, 640, 60))  # game start

    # Title
    win.blit(font_1.render('Voice Virtuoso', True,(242, 242, 242)),(175, 45))
    win.blit(font_2.render('', False, (0, 0, 0)), (350, 135))

    # Word Length
    word_length = 1
    win.blit(font_3.render('    CHOOSE THE LEVEL', True, (0, 0, 0)), (150, 210))

    pygame.draw.rect(win, (208, 83, 83), (170, 250, 85, 40))
    word_length_button_three = pygame.Rect(170, 250, 85, 40)
    win.blit(font_4.render('Letters', True, (255, 255, 255)), (185, 257))

    pygame.draw.rect(win, (255, 255, 255), (270, 250, 85, 40))
    word_length_button_four = pygame.Rect(270, 250, 85, 40)
    win.blit(font_4.render('Words', True, (208, 83, 83)), (292, 257))

    pygame.draw.rect(win, (255, 255, 255), (370, 250, 85, 40))
    word_length_button_random = pygame.Rect(370, 250, 85, 40)
    win.blit(font_4.render('Sentenses', True, (208, 83, 83)), (375, 257))

    # Time Limit
    time_limit = 3
    win.blit(font_3.render('CHOOSE TIME LIMIT', True, (0, 0, 0)), (180, 320))

    pygame.draw.rect(win, (208, 83, 83), (170, 360, 85, 40))
    time_limit_button_three = pygame.Rect(170, 360, 85, 40)
    win.blit(font_4.render('Three', True, (255, 255, 255)), (185, 367))

    pygame.draw.rect(win, (255, 255, 255), (270, 360, 85, 40))
    time_limit_button_five = pygame.Rect(270, 360, 85, 40)
    win.blit(font_4.render('Five', True, (208, 83, 83)), (292, 367))

    pygame.draw.rect(win, (255, 255, 255), (370, 360, 85, 40))
    time_limit_button_ten = pygame.Rect(370, 360, 85, 40)
    win.blit(font_4.render('Eight', True, (208, 83, 83)), (390, 367))

    speed = 1
    win.blit(font_3.render('Select The Speed', True, (0, 0, 0)), (180, 433))

    pygame.draw.rect(win, (255, 255, 255), (170, 473, 85, 40))
    n1 = pygame.Rect(170, 473, 85, 40)
    win.blit(font_4.render('0.25x', True, (208, 83, 83)), (185, 480))

    pygame.draw.rect(win, (255, 255, 255), (270, 473, 85, 40))
    n2 = pygame.Rect(270, 473, 85, 40)
    win.blit(font_4.render('0.5x', True, (208, 83, 83)), (292, 480))

    pygame.draw.rect(win, (208, 83, 83), (370, 473, 85, 40))
    n3 = pygame.Rect(370, 473, 85, 40)
    win.blit(font_4.render('1x', True, (255, 255, 255)), (390, 480))

    # Game Start
    win.blit(font_5.render('Game Start !!!', True, (208, 83, 83)), (247, 546))
    game_start_button = pygame.Rect(0, 546, 640, 60)


    # Action
    def word_length_button_three_pressed():
        pygame.draw.rect(win, (229, 143, 101), (0, 200, 640, 110))
        win.blit(font_3.render('    CHOOSE THE LEVEL', True, (0, 0, 0)), (150, 210))
        pygame.draw.rect(win, (208, 83, 83), (170, 250, 85, 40))
        win.blit(font_4.render('Letters', True, (255, 255, 255)), (185, 257))
        pygame.draw.rect(win, (255, 255, 255), (270, 250, 85, 40))
        win.blit(font_4.render('Words', True, (208, 83, 83)), (292, 257))
        pygame.draw.rect(win, (255, 255, 255), (370, 250, 85, 40))
        win.blit(font_4.render('Sentenses', True, (208, 83, 83)), (375, 257))

    def word_length_button_four_pressed():
        pygame.draw.rect(win, (229, 143, 101), (0, 200, 640, 110))
        win.blit(font_3.render('    CHOOSE THE LEVEL', True, (0, 0, 0)), (150, 210))
        pygame.draw.rect(win, (255, 255, 255), (170, 250, 85, 40))
        win.blit(font_4.render('Letters', True, (208, 83, 83)), (185, 257))
        pygame.draw.rect(win, (208, 83, 83), (270, 250, 85, 40))
        win.blit(font_4.render('Words', True, (255, 255, 255)), (292, 257))
        pygame.draw.rect(win, (255, 255, 255), (370, 250, 85, 40))
        win.blit(font_4.render('Sentenses', True, (208, 83, 83)), (375, 257))

    def get_voice_input():
        print("Please Speak....")
        recognizer = sr.Recognizer()
        with sr.Microphone() as source:
            audio_input = recognizer.listen(source)
            #print(audio_input)
        try:
            user_transcription = recognizer.recognize_google(audio_input)
            print(user_transcription)
            return user_transcription.lower()
        except sr.UnknownValueError:

            return None
        except sr.RequestError as e:

            return None
        
    def word_length_button_random_pressed():
        pygame.draw.rect(win, (229, 143, 101), (0, 200, 640, 110))
        win.blit(font_3.render('    CHOOSE THE LEVEL', True, (0, 0, 0)), (150, 210))
        pygame.draw.rect(win, (255, 255, 255), (170, 250, 85, 40))
        win.blit(font_4.render('Letters', True, (208, 83, 83)), (185, 257))
        pygame.draw.rect(win, (255, 255, 255), (270, 250, 85, 40))
        win.blit(font_4.render('Words', True, (208, 83, 83)), (292, 257))
        pygame.draw.rect(win, (208, 83, 83), (370, 250, 85, 40))
        win.blit(font_4.render('Sentenses', True, (255, 255, 255)), (375, 257))


    def time_limit_button_three_pressed():
        pygame.draw.rect(win, (249, 231, 132), (0, 310, 640, 110))
        win.blit(font_3.render('CHOOSE TIME LIMIT', True, (0, 0, 0)), (180, 320))
        pygame.draw.rect(win, (208, 83, 83), (170, 360, 85, 40))
        win.blit(font_4.render('Three', True, (255, 255, 255)), (185, 367))
        pygame.draw.rect(win, (255, 255, 255), (270, 360, 85, 40))
        win.blit(font_4.render('Five', True, (208, 83, 83)), (292, 367))
        pygame.draw.rect(win, (255, 255, 255), (370, 360, 85, 40))
        win.blit(font_4.render('Eight', True, (208, 83, 83)), (390, 367))


    def time_limit_button_five_pressed():
        pygame.draw.rect(win, (249, 231, 132), (0, 310, 640, 110))
        win.blit(font_3.render('CHOOSE TIME LIMIT', True, (0, 0, 0)), (180, 320))
        pygame.draw.rect(win, (255, 255, 255), (170, 360, 85, 40))
        win.blit(font_4.render('Three', True, (208, 83, 83)), (185, 367))
        pygame.draw.rect(win, (208, 83, 83), (270, 360, 85, 40))
        win.blit(font_4.render('Five', True, (255, 255, 255)), (292, 367))
        pygame.draw.rect(win, (255, 255, 255), (370, 360, 85, 40))
        win.blit(font_4.render('Eight', True, (208, 83, 83)), (390, 367))


    def time_limit_button_eight_pressed():
        pygame.draw.rect(win, (249, 231, 132), (0, 310, 640, 110))
        win.blit(font_3.render('CHOOSE TIME LIMIT', True, (0, 0, 0)), (180, 320))
        pygame.draw.rect(win, (255, 255, 255), (170, 360, 85, 40))
        win.blit(font_4.render('Three', True, (208, 83, 83)), (185, 367))
        pygame.draw.rect(win, (255, 255, 255), (270, 360, 85, 40))
        win.blit(font_4.render('Five', True, (208, 83, 83)), (292, 367))
        pygame.draw.rect(win, (208, 83, 83), (370, 360, 85, 40))
        win.blit(font_4.render('Eight', True, (255, 255, 255)), (390, 367))

    def n3p():
        pygame.draw.rect(win, (255, 255, 255), (170, 473, 85, 40))
        n1 = pygame.Rect(170, 473, 85, 40)
        win.blit(font_4.render('0.25x', True, (208, 83, 83)), (185, 480))

        pygame.draw.rect(win, (255, 255, 255), (270, 473, 85, 40))
        n2 = pygame.Rect(270, 473, 85, 40)
        win.blit(font_4.render('0.5x', True, (208, 83, 83)), (292, 480))

        pygame.draw.rect(win, (208, 83, 83), (370, 473, 85, 40))
        n3 = pygame.Rect(370, 473, 85, 40)
        win.blit(font_4.render('1x', True, (255, 255, 255)), (390, 480))

    def n2p():
        pygame.draw.rect(win, (255, 255, 255), (170, 473, 85, 40))
        n1 = pygame.Rect(170, 473, 85, 40)
        win.blit(font_4.render('0.25x', True, (208, 83, 83)), (185, 480))

        pygame.draw.rect(win, (208, 83, 83), (270, 473, 85, 40))
        n2 = pygame.Rect(270, 473, 85, 40)
        win.blit(font_4.render('0.5x', True, (255, 255, 255)), (292, 480))

        pygame.draw.rect(win, (255, 255, 255), (370, 473, 85, 40))
        n3 = pygame.Rect(370, 473, 85, 40)
        win.blit(font_4.render('1x', True, (208, 83, 83)), (390, 480))

    def n1p():
        pygame.draw.rect(win, (208, 83, 83), (170, 473, 85, 40))
        n1 = pygame.Rect(170, 473, 85, 40)
        win.blit(font_4.render('0.25x', True, (255, 255, 255)), (185, 480))

        pygame.draw.rect(win, (255, 255, 255), (270, 473, 85, 40))
        n2 = pygame.Rect(270, 473, 85, 40)
        win.blit(font_4.render('0.5x', True, (208, 83, 83)), (292, 480))

        pygame.draw.rect(win, (255, 255, 255), (370, 473, 85, 40))
        n3 = pygame.Rect(370, 473, 85, 40)
        win.blit(font_4.render('1x', True, (208, 83, 83)), (390, 480))
        
    # -----------------------------------------------------

    ##############
    # Game Start #
    ##############

    # Game Set Up


    life = 3


    def adj_en_char(en_char, en_char_x):
        if (en_char == "f") | (en_char == "i") | (en_char == "j") | (en_char == "l") | (en_char == "t"):
            return en_char_x + 15
        if (en_char == "r") | (en_char == "z"):
            return en_char_x + 5
        if en_char == "m":
            return en_char_x - 16
        if en_char == "w":
            return en_char_x - 10
        return en_char_x


    def adj_en_char2(en_char, en_char_x):
        if (en_char == "f") | (en_char == "i") | (en_char == "j") | (en_char == "l") | (en_char == "t"):
            return en_char_x + 10
        if (en_char == "r") | (en_char == "z"):
            return en_char_x + 5
        if en_char == "m":
            return en_char_x - 10
        if en_char == "w":
            return en_char_x - 10
        return en_char_x


    def show_card_three():
        win.fill((208, 83, 83))
        win.blit(font_1.render('Time', True, (242, 242, 242)), (215, 55))
        win.blit(font_1.render('Countdown', True, (242, 242, 242)), (145, 120))

        win.blit(font_2.render('Remember the words below :', True, (0, 0, 0)), (155, 235))


        pygame.draw.rect(win, (249, 231, 132), (270, 270, 100, 160))


        en_char_1_x = 290

        en_char_0_x = adj_en_char(correct_ans[0], en_char_1_x)

        win.blit(font_6.render(correct_ans[0], True, (255, 255, 255)), (en_char_1_x, 270))



    def show_card_four():
        win.fill((208, 83, 83))
        win.blit(font_1.render('Time', True, (242, 242, 242)), (215, 55))
        win.blit(font_1.render('Countdown', True, (242, 242, 242)), (145, 120))

        win.blit(font_2.render('Remember the words below :', True, (0, 0, 0)), (155, 235))
        pygame.draw.rect(win, (242, 242, 242), (85, 280, 100, 160))
        pygame.draw.rect(win, (249, 231, 132), (75, 270, 100, 160))
        pygame.draw.rect(win, (242, 242, 242), (215, 280, 100, 160))
        pygame.draw.rect(win, (249, 231, 132), (205, 270, 100, 160))
        pygame.draw.rect(win, (242, 242, 242), (345, 280, 100, 160))
        pygame.draw.rect(win, (249, 231, 132), (335, 270, 100, 160))
        pygame.draw.rect(win, (242, 242, 242), (475, 280, 100, 160))
        pygame.draw.rect(win, (249, 231, 132), (465, 270, 100, 160))
        en_char_0_x = 95
        en_char_1_x = 225
        en_char_2_x = 355
        en_char_3_x = 485
        en_char_0_x = adj_en_char(correct_ans[0], en_char_0_x)
        en_char_1_x = adj_en_char(correct_ans[1], en_char_1_x)
        en_char_2_x = adj_en_char(correct_ans[2], en_char_2_x)
        en_char_3_x = adj_en_char(correct_ans[3], en_char_3_x)
        win.blit(font_6.render(correct_ans[0], True, (255, 255, 255)), (en_char_0_x, 270))
        win.blit(font_6.render(correct_ans[1], True, (255, 255, 255)), (en_char_1_x, 270))
        win.blit(font_6.render(correct_ans[2], True, (255, 255, 255)), (en_char_2_x, 270))
        win.blit(font_6.render(correct_ans[3], True, (255, 255, 255)), (en_char_3_x, 270))



    word_one_button = pygame.Rect(30, 270, 80, 120)
    word_two_button = pygame.Rect(130, 270, 80, 120)
    word_three_button = pygame.Rect(230, 270, 80, 120)
    word_four_button = pygame.Rect(330, 270, 80, 120)
    word_five_button = pygame.Rect(430, 270, 80, 120)
    word_six_button = pygame.Rect(530, 270, 80, 120)
    confirm_button = pygame.Rect(200, 415, 110, 40)
    reset_button = pygame.Rect(330, 415, 110, 40)


    def three_choose_from_six():
        win.fill((208, 83, 83))

        win.blit(font_2.render('Please choose the words below :', True, (0, 0, 0)), (140, 50))

        pygame.draw.rect(win, (148, 148, 148), (270, 85, 100, 160))


        pygame.draw.rect(win, (242, 242, 242), (35, 275, 80, 120))
        pygame.draw.rect(win, (249, 231, 132), (30, 270, 80, 120))

        pygame.draw.rect(win, (242, 242, 242), (135, 275, 80, 120))
        pygame.draw.rect(win, (249, 231, 132), (130, 270, 80, 120))

        pygame.draw.rect(win, (242, 242, 242), (235, 275, 80, 120))
        pygame.draw.rect(win, (249, 231, 132), (230, 270, 80, 120))

        pygame.draw.rect(win, (242, 242, 242), (335, 275, 80, 120))
        pygame.draw.rect(win, (249, 231, 132), (330, 270, 80, 120))

        pygame.draw.rect(win, (242, 242, 242), (435, 275, 80, 120))
        pygame.draw.rect(win, (249, 231, 132), (430, 270, 80, 120))

        pygame.draw.rect(win, (242, 242, 242), (535, 275, 80, 120))
        pygame.draw.rect(win, (249, 231, 132), (530, 270, 80, 120))

        en_char_0_x = 47
        en_char_1_x = 147
        en_char_2_x = 247
        en_char_3_x = 347
        en_char_4_x = 447
        en_char_5_x = 547
        en_char_0_x = adj_en_char2(six_eng_characters_display[0], en_char_0_x)
        en_char_1_x = adj_en_char2(six_eng_characters_display[1], en_char_1_x)
        en_char_2_x = adj_en_char2(six_eng_characters_display[2], en_char_2_x)
        en_char_3_x = adj_en_char2(six_eng_characters_display[3], en_char_3_x)
        en_char_4_x = adj_en_char2(six_eng_characters_display[4], en_char_4_x)
        en_char_5_x = adj_en_char2(six_eng_characters_display[5], en_char_5_x)
        win.blit(font_7.render(six_eng_characters_display[0], True, (255, 255, 255)), (en_char_0_x, 270))
        win.blit(font_7.render(six_eng_characters_display[1], True, (255, 255, 255)), (en_char_1_x, 270))
        win.blit(font_7.render(six_eng_characters_display[2], True, (255, 255, 255)), (en_char_2_x, 270))
        win.blit(font_7.render(six_eng_characters_display[3], True, (255, 255, 255)), (en_char_3_x, 270))
        win.blit(font_7.render(six_eng_characters_display[4], True, (255, 255, 255)), (en_char_4_x, 270))
        win.blit(font_7.render(six_eng_characters_display[5], True, (255, 255, 255)), (en_char_5_x, 270))

        pygame.draw.rect(win, (255, 255, 255), (200, 415, 110, 40))
        win.blit(font_4.render('Speak', True, (208, 83, 83)), (220, 422))
        pygame.draw.rect(win, (255, 255, 255), (330, 415, 110, 40))
        win.blit(font_4.render('Reset', True, (208, 83, 83)), (360, 422))
        win.blit(font_2.render('Mark : '+str(mark), True, (0, 0, 0)), (510, 10))
        win.blit(font_2.render('Life : '+str(life), True, (0, 0, 0)), (20, 10))


    def four_choose_from_six():
        win.fill((208, 83, 83))

        win.blit(font_2.render('Please choose the words below :', True, (0, 0, 0)), (140, 50))
        pygame.draw.rect(win, (148, 148, 148), (75, 85, 100, 160))
        pygame.draw.rect(win, (148, 148, 148), (205, 85, 100, 160))
        pygame.draw.rect(win, (148, 148, 148), (335, 85, 100, 160))
        pygame.draw.rect(win, (148, 148, 148), (465, 85, 100, 160))

        pygame.draw.rect(win, (242, 242, 242), (35, 275, 80, 120))
        pygame.draw.rect(win, (249, 231, 132), (30, 270, 80, 120))

        pygame.draw.rect(win, (242, 242, 242), (135, 275, 80, 120))
        pygame.draw.rect(win, (249, 231, 132), (130, 270, 80, 120))

        pygame.draw.rect(win, (242, 242, 242), (235, 275, 80, 120))
        pygame.draw.rect(win, (249, 231, 132), (230, 270, 80, 120))

        pygame.draw.rect(win, (242, 242, 242), (335, 275, 80, 120))
        pygame.draw.rect(win, (249, 231, 132), (330, 270, 80, 120))

        pygame.draw.rect(win, (242, 242, 242), (435, 275, 80, 120))
        pygame.draw.rect(win, (249, 231, 132), (430, 270, 80, 120))

        pygame.draw.rect(win, (242, 242, 242), (535, 275, 80, 120))
        pygame.draw.rect(win, (249, 231, 132), (530, 270, 80, 120))

        en_char_0_x = 47
        en_char_1_x = 147
        en_char_2_x = 247
        en_char_3_x = 347
        en_char_4_x = 447
        en_char_5_x = 547
        en_char_0_x = adj_en_char2(six_eng_characters_display[0], en_char_0_x)
        en_char_1_x = adj_en_char2(six_eng_characters_display[1], en_char_1_x)
        en_char_2_x = adj_en_char2(six_eng_characters_display[2], en_char_2_x)
        en_char_3_x = adj_en_char2(six_eng_characters_display[3], en_char_3_x)
        en_char_4_x = adj_en_char2(six_eng_characters_display[4], en_char_4_x)
        en_char_5_x = adj_en_char2(six_eng_characters_display[5], en_char_5_x)
        win.blit(font_7.render(six_eng_characters_display[0], True, (255, 255, 255)), (en_char_0_x, 270))
        win.blit(font_7.render(six_eng_characters_display[1], True, (255, 255, 255)), (en_char_1_x, 270))
        win.blit(font_7.render(six_eng_characters_display[2], True, (255, 255, 255)), (en_char_2_x, 270))
        win.blit(font_7.render(six_eng_characters_display[3], True, (255, 255, 255)), (en_char_3_x, 270))
        win.blit(font_7.render(six_eng_characters_display[4], True, (255, 255, 255)), (en_char_4_x, 270))
        win.blit(font_7.render(six_eng_characters_display[5], True, (255, 255, 255)), (en_char_5_x, 270))

        pygame.draw.rect(win, (255, 255, 255), (200, 415, 110, 40))
        win.blit(font_4.render('Speak', True, (208, 83, 83)), (220, 422))
        pygame.draw.rect(win, (255, 255, 255), (330, 415, 110, 40))
        win.blit(font_4.render('Reset', True, (208, 83, 83)), (360, 422))
        win.blit(font_2.render('Mark : '+str(mark), True, (0, 0, 0)), (510, 10))
        win.blit(font_2.render('Life : '+str(life), True, (0, 0, 0)), (20, 10))


    def word_one_button_pressed():
        pygame.draw.rect(win, (100, 100, 100), (30, 270, 80, 120))


    def word_two_button_pressed():
        pygame.draw.rect(win, (100, 100, 100), (130, 270, 80, 120))


    def word_three_button_pressed():
        pygame.draw.rect(win, (100, 100, 100), (230, 270, 80, 120))


    def word_four_button_pressed():
        pygame.draw.rect(win, (100, 100, 100), (330, 270, 80, 120))


    def word_five_button_pressed():
        pygame.draw.rect(win, (100, 100, 100), (430, 270, 80, 120))


    def word_six_button_pressed():
        pygame.draw.rect(win, (100, 100, 100), (530, 270, 80, 120))


    correct_ans = []
    position = 0
    choose_ans = []
    word_one_idx = 0
    word_two_idx = 0
    word_three_idx = 0
    word_four_idx = 0
    word_five_idx = 0
    word_six_idx = 0


    def word_selected(pos, en_char):
        if len(correct_ans) == 1:

                pygame.draw.rect(win, (255, 255, 255), (270, 85, 100, 160))
                en_char_x = 290
                en_char_x = adj_en_char(en_char, en_char_x)
                win.blit(font_6.render(en_char, True, (208, 83, 83)), (en_char_x, 85))


        if len(correct_ans) == 4:
            if pos == 0:
                pygame.draw.rect(win, (255, 255, 255), (75, 85, 100, 160))
                en_char_x = 95
                en_char_x = adj_en_char(en_char, en_char_x)
                win.blit(font_6.render(en_char, True, (208, 83, 83)), (en_char_x, 85))
            if pos == 1:
                pygame.draw.rect(win, (255, 255, 255), (205, 85, 100, 160))
                en_char_x = 225
                en_char_x = adj_en_char(en_char, en_char_x)
                win.blit(font_6.render(en_char, True, (208, 83, 83)), (en_char_x, 85))
            if pos == 2:
                pygame.draw.rect(win, (255, 255, 255), (335, 85, 100, 160))
                en_char_x = 355
                en_char_x = adj_en_char(en_char, en_char_x)
                win.blit(font_6.render(en_char, True, (208, 83, 83)), (en_char_x, 85))
            if pos == 3:
                pygame.draw.rect(win, (255, 255, 255), (465, 85, 100, 160))
                en_char_x = 485
                en_char_x = adj_en_char(en_char, en_char_x)
                win.blit(font_6.render(en_char, True, (208, 83, 83)), (en_char_x, 85))

    a1,a2 = '',[]
    next_button = pygame.Rect(0, 420, 640, 60)
    replay_button_rect = pygame.Rect(0, 500, 640, 60)
    music_three_button = pygame.Rect(60, 314, 80, 80)
    music_four_button = pygame.Rect(30, 314, 80, 80)


    def correct_match(speed=1,word=[]):
        global a1,a2
        words = word
        words[0] = word[0].upper()
        play_word_videos(video_dir, words)
        a1,a2 = video_dir, words
        pygame.display.update()
        win.fill((255, 255, 255))
        words[0] = word[0].lower()
        file_path = [item for item in [item for item in os.listdir(image_dir) if ''.join(correct_ans) in item] if os.path.splitext(item)[0] == ''.join(correct_ans)][0]
        
        image_path = os.path.join(image_dir, file_path)
        im = Image.open(image_path)
        width, height = im.size
        new_width = int(280*width/height)
        word_image = pygame.image.load(image_path)
        word_image = pygame.transform.scale(word_image, (new_width, 280))
        new_x = int((640 - new_width)/2)
        win.blit(word_image, (new_x, 10))
        pygame.draw.rect(win, (235, 238, 244), (0, 420, 640, 60))
        win.blit(font_5.render('Next', True, (208, 83, 83)), (310, 433))

        pygame.draw.rect(win, (208, 83, 83), replay_button_rect)
        win.blit(font_5.render('Replay', True, (255, 255, 255)), (310, 530))

        if len(correct_ans) == 1:
            en_char_0_x = 290

            en_char_0_x = adj_en_char(correct_ans[0], en_char_0_x)

            win.blit(font_6.render(correct_ans[0], True, (100, 100, 100)), (en_char_0_x, 270))

            music_button = pygame.image.load('music_button.png')
            music_button = pygame.transform.scale(music_button, (80, 80))
            win.blit(music_button, (60, 314))

        if len(correct_ans) == 4:
            en_char_0_x = 125
            en_char_1_x = 235
            en_char_2_x = 345
            en_char_3_x = 465
            en_char_0_x = adj_en_char(correct_ans[0], en_char_0_x)
            en_char_1_x = adj_en_char(correct_ans[1], en_char_1_x)
            en_char_2_x = adj_en_char(correct_ans[2], en_char_2_x)
            en_char_3_x = adj_en_char(correct_ans[3], en_char_3_x)
            win.blit(font_6.render(correct_ans[0], True, (100, 100, 100)), (en_char_0_x, 270))
            win.blit(font_6.render(correct_ans[1], True, (100, 100, 100)), (en_char_1_x, 270))
            win.blit(font_6.render(correct_ans[2], True, (100, 100, 100)), (en_char_2_x, 270))
            win.blit(font_6.render(correct_ans[3], True, (100, 100, 100)), (en_char_3_x, 270))
            music_button = pygame.image.load('music_button.png')
            music_button = pygame.transform.scale(music_button, (80, 80))
            win.blit(music_button, (30, 314))

    restart_button = pygame.Rect(200, 265, 110, 40)
    quit_button = pygame.Rect(330, 265, 110, 40)


    def game_over():
        win.fill((208, 83, 83))
        win.blit(font_6.render('Game Over', True, (0, 0, 0)), (50, 10))
        win.blit(font_1.render('Total Mark', True, (0, 0, 0)), (130, 160))
        win.blit(font_1.render(str(mark), True, (0, 0, 0)), (430, 160))
        pygame.draw.rect(win, (255, 255, 255), (200, 265, 110, 40))
        win.blit(font_4.render('Restart', True, (208, 83, 83)), (220, 272))
        pygame.draw.rect(win, (255, 255, 255), (330, 265, 110, 40))
        win.blit(font_4.render('Quit', True, (208, 83, 83)), (365, 272))


    def restart():
        # Background
        win.fill((208, 83, 83))  # title
        pygame.draw.rect(win, (229, 143, 101), (0, 200, 640, 110))  # word length
        pygame.draw.rect(win, (249, 231, 132), (0, 310, 640, 110))  # time limit
        pygame.draw.rect(win, (249, 231, 180), (0, 420, 640, 110))  # time limit
        pygame.draw.rect(win, (235, 238, 244), (0, 530, 640, 60))  # game start

        # Title
        win.blit(font_1.render('Voice Virtuoso', True,(242, 242, 242)),(175, 45))
        win.blit(font_2.render('', False, (0, 0, 0)), (350, 135))

        # Word Length
        word_length = 1
        win.blit(font_3.render('    CHOOSE THE LEVEL', True, (0, 0, 0)), (150, 210))

        pygame.draw.rect(win, (208, 83, 83), (170, 250, 85, 40))
        word_length_button_three = pygame.Rect(170, 250, 85, 40)
        win.blit(font_4.render('Letters', True, (255, 255, 255)), (185, 257))

        pygame.draw.rect(win, (255, 255, 255), (270, 250, 85, 40))
        word_length_button_four = pygame.Rect(270, 250, 85, 40)
        win.blit(font_4.render('Words', True, (208, 83, 83)), (292, 257))

        pygame.draw.rect(win, (255, 255, 255), (370, 250, 85, 40))
        word_length_button_random = pygame.Rect(370, 250, 85, 40)
        win.blit(font_4.render('Sentenses', True, (208, 83, 83)), (375, 257))

        # Time Limit
        time_limit = 3
        win.blit(font_3.render('CHOOSE TIME LIMIT', True, (0, 0, 0)), (180, 320))

        pygame.draw.rect(win, (208, 83, 83), (170, 360, 85, 40))
        time_limit_button_three = pygame.Rect(170, 360, 85, 40)
        win.blit(font_4.render('Three', True, (255, 255, 255)), (185, 367))

        pygame.draw.rect(win, (255, 255, 255), (270, 360, 85, 40))
        time_limit_button_five = pygame.Rect(270, 360, 85, 40)
        win.blit(font_4.render('Five', True, (208, 83, 83)), (292, 367))

        pygame.draw.rect(win, (255, 255, 255), (370, 360, 85, 40))
        time_limit_button_ten = pygame.Rect(370, 360, 85, 40)
        win.blit(font_4.render('Eight', True, (208, 83, 83)), (390, 367))

        speed = 1
        win.blit(font_3.render('Select The Speed', True, (0, 0, 0)), (180, 433))

        pygame.draw.rect(win, (255, 255, 255), (170, 473, 85, 40))
        n1 = pygame.Rect(170, 473, 85, 40)
        win.blit(font_4.render('0.25x', True, (208, 83, 83)), (185, 480))

        pygame.draw.rect(win, (255, 255, 255), (270, 473, 85, 40))
        n2 = pygame.Rect(270, 473, 85, 40)
        win.blit(font_4.render('0.5x', True, (208, 83, 83)), (292, 480))

        pygame.draw.rect(win, (208, 83, 83), (370, 473, 85, 40))
        n3 = pygame.Rect(370, 473, 85, 40)
        win.blit(font_4.render('1x', True, (255, 255, 255)), (390, 480))

        # Game Start
        win.blit(font_5.render('Game Start !!!', True, (208, 83, 83)), (247, 546))
        game_start_button = pygame.Rect(0, 546, 640, 60)

    # -------------------------------------------------------

    run = True
    while run:
        pygame.time.delay(100)
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                run = False

            if life == 0:
                page = 4
                game_over()

            if page == 1:
                if event.type == pygame.USEREVENT:
                    time_count -= 1
                time_text = int(time_count)
                if time_text > time_limit:
                    time_text = time_limit
                pygame.draw.rect(win, (208, 83, 83), (420, 50, 100, 160))
                win.blit(font_6.render(str(time_text), True, (242, 242, 242)), (440, 50))
                pygame.display.flip()
                clock.tick(60)
                if time_count <= 0:
                    page = 2
                    position = 0
                    choose_ans = []
                    if len(correct_ans) == 1:
                        three_choose_from_six()
                    if len(correct_ans) == 4:
                        four_choose_from_six()

            if event.type == pygame.MOUSEBUTTONDOWN:
                
                mouse_pos = event.pos
                if (word_length_button_three.collidepoint(mouse_pos)) & (page == 0):
                    flag = False
                    word_length = 1
                    word_length_button_three_pressed()
                if (word_length_button_four.collidepoint(mouse_pos)) & (page == 0):
                    flag = False
                    word_length = 5
                    word_length_button_four_pressed()
                if (word_length_button_random.collidepoint(mouse_pos)) & (page == 0):
                    flag = True
                    word_length_button_random_pressed()


                if (time_limit_button_three.collidepoint(mouse_pos)) & (page == 0):
                    time_limit = 3
                    time_limit_button_three_pressed()
                if (time_limit_button_five.collidepoint(mouse_pos)) & (page == 0):
                    time_limit = 5
                    time_limit_button_five_pressed()
                if (time_limit_button_ten.collidepoint(mouse_pos)) & (page == 0):
                    time_limit = 8
                    time_limit_button_eight_pressed()
                if (n3.collidepoint(mouse_pos)) & (page == 0):
                    speed = 1
                    n3p()
                if (n1.collidepoint(mouse_pos)) & (page == 0):
                    speed = 0.25
                    n1p()
                if (n2.collidepoint(mouse_pos)) & (page == 0):
                    speed = 0.5
                    n2p()
                if (game_start_button.collidepoint(mouse_pos)) & (page == 0):
                    if flag==False:
                        game_df = word_df.copy()
                        if word_length == 1:
                            game_df = game_df[game_df['Len'] == 1]
              
                        if word_length == 4:
                            game_df = game_df[game_df['Len'] == 4]
                        game_df = game_df.reset_index()
                        sequence = list(range(len(game_df)))  # number of words to play
                        random.shuffle(sequence)
                        idx = 0
                        mark = 0 
                        tries = 0
           
    
                        correct_ans = list(game_df['Word'][sequence[idx]])
                
                        random_idx = 6 - len(correct_ans)
                        eng_character = set(string.ascii_lowercase)
                        random_eng_character = list(eng_character.difference(set(correct_ans)))
                        random.shuffle(random_eng_character)
                        six_eng_characters_display = random_eng_character[:random_idx] + correct_ans
                        random.shuffle(six_eng_characters_display)
    
                        page = 1
                        time_count = time_limit + 1
                        if len(correct_ans) == 1:
                            show_card_three()
                        if len(correct_ans) == 4:
                            show_card_four()
                    else:

                        root = tk.Tk()
                        
                        game = SentencePhoneticsGame(root)
                        root.mainloop()

                if (word_one_button.collidepoint(mouse_pos)) & (page == 2) & (word_one_idx == 0):
                    if position < len(correct_ans):
                        word_one_button_pressed()
                        word_selected(position, six_eng_characters_display[0])
                        choose_ans = choose_ans + [six_eng_characters_display[0]]
                        word_one_idx += 1
                        position += 1

                if (word_two_button.collidepoint(mouse_pos)) & (page == 2) & (word_two_idx == 0):
                    if position < len(correct_ans):
                        word_two_button_pressed()
                        word_selected(position, six_eng_characters_display[1])
                        choose_ans = choose_ans + [six_eng_characters_display[1]]
                        word_two_idx += 1
                        position += 1

                if (word_three_button.collidepoint(mouse_pos)) & (page == 2) & (word_three_idx == 0):
                    if position < len(correct_ans):
                        word_three_button_pressed()
                        word_selected(position, six_eng_characters_display[2])
                        choose_ans = choose_ans + [six_eng_characters_display[2]]
                        word_three_idx += 1
                        position += 1

                if (word_four_button.collidepoint(mouse_pos)) & (page == 2) & (word_four_idx == 0):
                    if position < len(correct_ans):
                        word_four_button_pressed()
                        word_selected(position, six_eng_characters_display[3])
                        choose_ans = choose_ans + [six_eng_characters_display[3]]
                        word_four_idx += 1
                        position += 1

                if (word_five_button.collidepoint(mouse_pos)) & (page == 2) & (word_five_idx == 0):
                    if position < len(correct_ans):
                        word_five_button_pressed()
                        word_selected(position, six_eng_characters_display[4])
                        choose_ans = choose_ans + [six_eng_characters_display[4]]
                        word_five_idx += 1
                        position += 1

                if (word_six_button.collidepoint(mouse_pos)) & (page == 2) & (word_six_idx == 0):
                    if position < len(correct_ans):
                        word_six_button_pressed()
                        word_selected(position, six_eng_characters_display[5])
                        choose_ans = choose_ans + [six_eng_characters_display[5]]
                        word_six_idx += 1
                        position += 1

                if (confirm_button.collidepoint(mouse_pos)) & (page == 2):
                    
                    if position == (len(correct_ans)):

                        try:
                            word = get_voice_input()
                            if word==None:
                                word = ''
                            word = word.replace(" ",'').lower()
                            x = ''
                            for i in correct_ans:
                                x+=i
                            token_scores = calculate_token_scores(x, word)
                            for token, score in token_scores.items():
                                pass
                            
                            # Calculate and print the overall score
                            overall_score = calculate_overall_score(token_scores)
                        except:
                            overall_score = 1.0
                        if overall_score<0.4:
                            overall_score=0.4
                            
                        if choose_ans == correct_ans and overall_score>0.50:
                            mark += 1
                            page = 3
                            delay = 1
                            correct_match(overall_score,correct_ans)
                        else:
                            life -= 1
                            word_one_idx = 0
                            word_two_idx = 0
                            word_three_idx = 0
                            word_four_idx = 0
                            word_five_idx = 0
                            word_six_idx = 0
                            position = 0
                            choose_ans = []
                            if len(correct_ans) == 1:

                                three_choose_from_six()
                            if len(correct_ans) == 4:

                                four_choose_from_six()
                        if len(correct_ans) == 1:
                            database()

                            x = mark
                            if x>=9 and idx>=9:
                                res = tkMessageBox.askquestion("Phonetics App","You are going great job in this level, You can move to words now")
                                if res:
                                    pygame.quit()
                                    mainwindow()
                                else:
                                    pass
                            cursor.execute(f"UPDATE grade set letter='{x}' where id={userid}")
                            conn.commit()
                            conn.close()
                            
                        elif len(correct_ans) == 4:
                            database()
                            x = mark
                            if x>=9 and idx>=9:
                                res = tkMessageBox.askquestion("Phonetics App","You are going great job in this level, You can move to sentence now")
                                if res:
                                    pygame.quit()
                                    mainwindow()
                                else:
                                    pass
                            cursor.execute(f"UPDATE grade set letter='{x}' where id={userid}")
                            conn.commit()
                            conn.close()

                if (reset_button.collidepoint(mouse_pos)) & (page == 2):
                    word_one_idx = 0
                    word_two_idx = 0
                    word_three_idx = 0
                    word_four_idx = 0
                    word_five_idx = 0
                    word_six_idx = 0
                    position = 0
                    choose_ans = []
                    if len(correct_ans) == 1:
                        three_choose_from_six()
                    if len(correct_ans) == 4:
                        four_choose_from_six()

                if (music_three_button.collidepoint(mouse_pos)) & (page == 3) & (len(correct_ans) == 1):
                    music_file = ''.join(correct_ans) + '.mp3'
                    music_path = os.path.join(audio_dir, music_file)
                    mixer.music.load(music_path)
                    mixer.music.play()

                if (music_four_button.collidepoint(mouse_pos)) & (page == 3) & (len(correct_ans) == 4):
                    music_file = ''.join(correct_ans) + '.mp3'
                    music_path = os.path.join(audio_dir, music_file)
                    mixer.music.load(music_path)
                    mixer.music.play()

                if (replay_button_rect.collidepoint(mouse_pos)) & (page == 3):
            
                    play_word_videos(a1,a2)
                    if delay == 0:
                        idx += 1
                        word_one_idx = 0
                        word_two_idx = 0
                        word_three_idx = 0
                        word_four_idx = 0
                        word_five_idx = 0
                        word_six_idx = 0
                        choose_ans = []

                        correct_ans = list(game_df['Word'][sequence[idx]])
            
                        random_idx = 6 - len(correct_ans)
                        eng_character = set(string.ascii_lowercase)
                        random_eng_character = list(eng_character.difference(set(correct_ans)))
                        random.shuffle(random_eng_character)
                        six_eng_characters_display = random_eng_character[:random_idx] + correct_ans
                        random.shuffle(six_eng_characters_display)
             
                        page = 1
                        time_count = time_limit + 1
                        if len(correct_ans) == 1:

                            show_card_three()
                        if len(correct_ans) == 4:
                            show_card_four()
                    else:
                        delay = 0

                if (next_button.collidepoint(mouse_pos)) & (page == 3):
                    if delay == 0:
                        idx += 1
                        word_one_idx = 0
                        word_two_idx = 0
                        word_three_idx = 0
                        word_four_idx = 0
                        word_five_idx = 0
                        word_six_idx = 0
                        choose_ans = []
             
                        correct_ans = list(game_df['Word'][sequence[idx]])
        
                        random_idx = 6 - len(correct_ans)
                        eng_character = set(string.ascii_lowercase)
                        random_eng_character = list(eng_character.difference(set(correct_ans)))
                        random.shuffle(random_eng_character)
                        six_eng_characters_display = random_eng_character[:random_idx] + correct_ans
                        random.shuffle(six_eng_characters_display)
             
                        page = 1
                        time_count = time_limit + 1
                        if len(correct_ans) == 1:
                            show_card_three()
                        if len(correct_ans) == 4:
                            show_card_four()
                    else:
                        delay = 0

                if (restart_button.collidepoint(mouse_pos)) & (page == 4):
                    page = 0
                    life = 3
                    word_length = 5
                    time_limit = 3
                    restart()
                    mainwindow()

                if (quit_button.collidepoint(mouse_pos)) & (page == 4):
                    run = False

        pygame.display.update()

    pygame.quit()


    
signup()
#mainwindow()
