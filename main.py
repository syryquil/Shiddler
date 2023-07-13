import random
import re
import openai
import time

riddle_prompts = ["What is <adj> and <adj> and <adj> all over?",
                  "Why did the <noun> <verb> the <noun>?",
                  "How many <pl-noun> does it take to <verb> a <noun>?",
                  "I have <pl-noun> but no <noun> or <noun>. What am I?",
                  "I have four <pl-noun>, three <pl-noun>, and a <noun>. What am I?"]


def generate_riddle():
    blank = random.choice(riddle_prompts)
    regex = re.compile(r'<(.*?)>')

    tokens = blank.split()
    for i in range(len(tokens)):
        if re.match(regex, tokens[i]): #if fill in the blank spot found
            pos = tokens[i]
            pos = pos.lstrip('<')
            pos = pos.rstrip('>.,?!')

            with open(f'{pos}.txt') as f:
                lines = f.readlines()

            tokens[i] = (random.choice(lines)).strip() #replace with random matching part of speech

    riddle = ' '.join(tokens)
    return riddle

def generate_answer(riddle):

    openai.api_key = "api-key"

    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        temperature=0.8,
        max_tokens=2000,
        messages=[
            {"role": "system", "content": "You are tasked with answering riddles, giving no further elaboration beyond the answer itself."},
            {"role": "user", "content": "Answer this riddle: I have branches, but no fruit, trunk or leaves. What am I?"},
                {"role": "assistant", "content": "A bank."},
            {"role": "user", "content": f"Answer this riddle: {riddle}"}
        ]
    )

    return completion.choices[0].message["content"]

already_answered = False
while True:

    #prompt for new riddle

    query = ""
    if already_answered:
        query = input("What fun! Would you like to answer another? \n")
    else:
        query = input("Hello!! My name is the shiddler! Do you want to answer a riddle ahahahaha? \n")

    while True:
        query = query[0].lower()

        if (query != 'y') and (query != 'n'):
            query = query('Please answer with yes or no! \n')
        elif query == 'n':
            print('well fuck you then! Bye')
            time.sleep(3)
            quit()
        elif query == 'y':
            break

    riddle = generate_riddle()
    answer = generate_answer(riddle)

    #give player 3 chances
    chances = 3
    times_attempted = 0

    response = input(f"Answer this riddle, if you dare: {riddle} \n")
    while times_attempted < chances:
        if response.lower().rstrip(".?!") == answer.lower().rstrip(".?!"):
            print("Correct! Congrats on solving my puzzle. \n")
            break
        else:
            times_attempted += 1
            if times_attempted < 3:
                response = input(f"Nope! You have {3 - times_attempted} more attempts. Try again: \n")
            else:
                print(f"You failed! The correct answer was {answer}. \n")

    already_answered = True