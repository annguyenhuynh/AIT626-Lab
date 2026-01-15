"""
Name: An Huynh
Course: AIT 626 - 003
Assignment: Eliza Chatbot
"""

import random
import re

#--------------------------------
# Reflections for mirroring users
# Reflections dictionary used to swap pronouns and verbs, to mirror user input.
#--------------------------------
reflections = {
    "am": "are",
    "was": "were",
    "i": "you",
    "i'd": "you would",
    "i've": "you have",
    "i'll": "you will",
    "my": "your",
    "are": "am",
    "you": "I",
    "you'd": "I would",
    "you've": "I have",
    "you'll": "I will",
    "your": "my",
    "yours": "mine",
    "me": "you"
}

#--------------------------------
# Word Spotting
# The following keywords dictionary show common emotions in therapy-style conversations.
# The key is the keyword to spot, and the value is a list of possible responses.
#--------------------------------
keywords = {
    "sad": ["Why do you feel said?", "What makes you feel sad?", "Do you often feel sad?"],
    "happy": ["What makes you feel happy?", "Why do you feel happy?", "Do you often feel happy?"],
    "stress": ["What is causing your stress?", "How do you usually deal with stress?", "Do you feel stressed often?"],
    "love": ["Who or what do you love?","What does love mean to you?", "How do you express love?", "Do you feel loved?"],
    "hate": ["What makes you feel hate?", "How do you cope with feelings of hate?", "Do you often feel hate?", "Do you think people hate you?"],
    "depressed": ["Have you been feeling depressed for a long time?", "What do you think is causing your depression?", "Have you talked to anyone about your depression?"],
    "anxious": ["What makes you feel anxious?", "How do you usually handle anxiety?", "Do you often feel anxious?"]
}

event_kw = {
    "money_positive": {
        "keywords": ["bonus","raise","paid","promotion","salary","refund","grant","scholarship"],
        "responses": [
            "That’s wonderful news, {name}! Financial wins can really lift your mood. What does this mean for you?",
            "Congratulations, {name}! How are you thinking of using this money?",
            "That sounds like a big relief. Does this change any plans you had?"
        ]
    },
    "achievements": {
        "keywords": ["passed","graduated","accepted","won","certified","finished","completed"],
        "responses": [
            "That’s a great accomplishment, {name}! What part was the hardest?",
            "You should be proud of yourself. How does achieving this make you feel?",
            "That’s exciting — what’s your next goal?"
        ]
    },
    "relationship_negative": {
        "keywords": ["breakup","divorce","separated","argument","fight"],
        "responses": [
            "I’m sorry you’re going through that. Want to talk about what happened?",
            "That sounds painful. How have you been coping?"
        ]
    },
    "work_stress": {
        "keywords": ["deadline","burnout","overworked","micromanage","pressure"],
        "responses": [
            "That sounds stressful. What’s been weighing on you the most at work?",
            "How long has this been going on?"
        ]
    },
    "health": {
        "keywords": ["sick","hospital","injured","pain","diagnosed"],
        "responses": [
            "That must be difficult. How are you feeling physically and emotionally?",
            "I’m sorry you’re dealing with that. Do you have support right now?"
        ]
    }
}


#--------------------------------
# Default Reposnses
# The list of the responses is used when:
    # No keyword is detected
    # No sentence pattern match
    # The input contains gibberish or too complicated
#--------------------------------
default_responses = [
    "Can you tell me more about that?",
    "How does that make you feel?",
    "Why do you say that?",
    "What do you think about that?",
    "Can you elaborate on that?",
    "How long have you felt this way?"
]

#--------------------------------
# Function to reflect pronouns
#--------------------------------
def reflect(fragment):
    words = fragment.lower().split()
    reflected_words = [reflections.get(word,word) for word in words]
    return ' '.join(reflected_words)

#--------------------------------
# Function to detect events
#--------------------------------
def detect_event(text):
    text = text.lower()
    for data in event_kw.values():
        for kw in data["keywords"]:
            if re.search(rf"\b{kw}\b", text):
                return data
    return None

#--------------------------------
# Function to infer emotions
#--------------------------------
def infer_emotions(text):
    POS = ["good","great","awesome","excited","relieved","happy","nice"]
    NEG = ["bad","terrible","tired","stressed","upset","sad"]
    text = text.lower()
    for w in POS:
        if re.search(rf"\b{w}\b", text):
            return "happy"
    for w in NEG:
        if re.search(rf"\b{w}\b", text):
            return "sad"
    return None


#--------------------------------
# Process user input and response
#--------------------------------

def eliza_response(user_input, name):
    user_input = user_input.strip()
    event = detect_event(user_input)
    if event:
        return random.choice(event['responses']).format(name=name)
    emotion = infer_emotions(user_input)
    if emotion == "happy":
        return f"That's good to hear, {name}. Can you share more?"
    if emotion == "sad":
        return f"I'm sorry to hear that, {name}. Do you want to tell me more?"

    for key, response in keywords.items():
        # Using rf as raw f string (backlash is backlash)
        if re.search(rf"\b{key}\b", user_input, re.I):
            return random.choice(response)
        
        # Sentence Transformation patterns

    # Pattern 1: I feel...
    match = re.match(r".*\bi feel (.*)", user_input, re.I)
    if match:
        feeling = reflect(match.group(1))
        return f"Why do you feel {feeling}, {name}?"
    
    # Pattern 2: I am...
    match = re.match(r".*\bi am (.*)", user_input, re.I)
    if match:  
        state = reflect(match.group(1))
        return f"How long have you been {state}, {name}?"

    # Pattern 3: my <person / thing / place>
    match = re.match(r".*\bmy (.*)", user_input, re.I)
    if match:
        subject = match.group(1)
        return f"How does your {subject} affect you?" 
    
    # Pattern 4: generic I ...
    match = re.match(r".*\bi (.*)", user_input, re.I)
    if match:
        action = reflect(match.group(1))
        return f"Why do you say that you {action}, {name}?"
        
    #--------------------------------
    # Gibberish Handling
    #--------------------------------

    # If input is empty or contains only symbols
    if not re.search(r"[a-zA-Z]", user_input):
        return "I'm sorry, I didn't catch that. Could you please elaborate?"
    
    # If input is too long or complex (more than 20 words)
    if len(user_input.split()) > 20:
        return "That's quite a lot to take in. Could you please simplify your thoughts?"
    
    # Fallback responses
    return random.choice(default_responses)
        
#--------------------------------
# Main dialogue loop
#--------------------------------
def eliza():
    print("Hello, I'm Eliza, your virtual therapist. What's your name?")
    name = input().strip()
    print(f"Nice to meet you, {name}. How are you feeling today?")

    while True:
        user_input = input("=> ")

        if user_input.lower() in ["bye", "exit", "quit"]:
            print("Goodbye! Take care of yourself.")
            break
        response = eliza_response(user_input, name)
        print(response)
if __name__ == "__main__":
    eliza()
