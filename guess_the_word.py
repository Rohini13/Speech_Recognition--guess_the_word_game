import random
import time
import speech_recognition as sr

def recognize_from_mic(recognizer,microphone):
    if not isinstance(recognizer,sr.Recognizer):
        raise TypeError("`recognizer` must be an instance of `Recognizer`")
    if not isinstance(microphone,sr.Microphone):
        raise TypeError("`microphone` must be ab instance of `Microphone`")

    with microphone as source:
        recognizer.adjust_for_ambient_noise(source)
        audio=recognizer.listen(source)

    response = {
        "success": True,
        "error": None,
        "transcription": None
    }
    try:
        response["transcription"]=recognizer.recognize_google(audio)
    except sr.RequestError:
        response["success"]=False
        response["error"]="API not available"
    except sr.UnknownValueError:
        response["error"]="Unable to recognize Speech"
    return response

if __name__=="__main__":
    words=["green","orange","yellow","blue","pink","black","white","brown"]
    num_guesses=3
    prompt_limit=5
    
    recognizer=sr.Recognizer()
    microphone=sr.Microphone()
    
    word=random.choice(words)
    instructions = (
        "I'm thinking of one of these words:\n"
        "{words}\n"
        "You have {n} tries to read my mind.\n"
    ).format(words=', '.join(words), n=num_guesses)

    print(instructions)
    time.sleep(3)

    for i in range(num_guesses):
        for j in range(prompt_limit):
            print('Guess {}. Speak!'.format(i+1))
            guess = recognize_from_mic(recognizer, microphone)
            if guess["transcription"]:
                break
            if not guess["success"]:
                break
            print("I didn't catch that. What did you say?\n")

        if guess["error"]:
            print("ERROR: {}".format(guess["error"]))
            break

        print("You said: {}".format(guess["transcription"]))

        is_correct_guess=guess["transcription"].lower()==word.lower()
        is_guess_left=i<num_guesses-1

        if is_correct_guess:
            print("Correct! You win!".format(word))
            break
        elif is_guess_left:
            print("Incorrect. Try again.\n")
        else:
            print("Sorry, you lose!\nI was thinking of '{}'.".format(word))
            break