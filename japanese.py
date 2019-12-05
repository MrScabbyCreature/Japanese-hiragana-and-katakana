import pandas as pd
import numpy as np
from random import shuffle
from IPython.display import display as display_dataframe

df = pd.read_excel("hira-kata.xlsx")
japanese_columns = ['hiragana', 'katakana']
probability_columns = {'hiragana': 'hira_prob', 'katakana': 'kata_prob'}
if 'hira_prob' not in df.columns or 'kata_prob' not in df.columns:
    df['hira_prob'] = 1.0
    df['kata_prob'] = 1.0

def random_index(column):
    prob_col = probability_columns[column]
    probability = np.random.random() * df[prob_col].sum()
    index = 0
    for i in range(df.shape[0]):
        probability -= df[prob_col][i]
        if probability <= 0:
            index = i
            break
    return index

def ask_MCQ(index, column):
    character = df[column][index]
    english = df['english'][index]

    #getting random options
    randomized_choices = list(df['english'])
    randomized_choices.remove(english)
    shuffle(randomized_choices)
    choices = [english] + randomized_choices[:3]
    shuffle(choices)

    #ask the question
    print("The pronounciation of {} is:".format(character))
    for i in range(4):
        print(str(i) + ") {}".format(choices[i]))
    answer = input()
    try:
        if choices[int(answer)] == english:
            print("Correct!")
            return True
        else:
            print("Oops! The answer is {}".format(english))
            return False
    except Exception as e:
        print(e)
        print("Kya input karrela bhailog... -_-")

def ask_blank(index, column):
    character = df[column][index]
    english = df['english'][index]

    #ask the question
    print("What is the pronounciation of {}?".format(character))
    print("Show answer? (Y)")
    input()
    print("Answer is: {}".format(english))
    print("Did you get it right?")
    choices = ['Yes!', 'No :(']
    for i in range(2):
        print(str(i) + ") {}".format(choices[i]))
    answer = input()
    try:
        if choices[int(answer)] == choices[0]:
            print("Nice!")
            return True
        else:
            print("It's okay. Next time!")
            return False
    except Exception as e:
        print("Kya input karrela bhailog... -_-")

function = [ask_blank, ask_MCQ]
prob_change = [[1.5, 0.5],
               [1.1, 0.9]]

#main loop
while True:
    # do hiragana
    # column = japanese_columns[0]
    # do katakana
    # column = japanese_columns[1]
    # do both randomly
    column = japanese_columns[int(np.random.random()*2)]

    index = random_index(column)
    random_choice = (np.random.random() <= df[probability_columns[column]][index])
    result = function[random_choice](index, column)
    if result is not None:
        df.loc[index, probability_columns[column]] *= prob_change[random_choice][result]
    print("\n\n")
    df.to_excel("hira-kata.xlsx")
    # display_dataframe(df)
