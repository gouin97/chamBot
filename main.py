#####################
# Copyright Gouin97 #
#####################

import json
import random
import time

def  ai(dataFileToUse, botName, error):
    '''
    Description: Function that reads the user input, compares it with answers in the json data file and responds.
    Inputs :
        - dataFileToUse: Specifies the name of the json file to use as data (string)
        - botName: Specifies the name of the bot which will be printed in the dialog box (string)
        - error: Specifies the string to return if the bot does not know what to answer (string)
    '''
    with open (dataFileToUse) as myfile:
        data = json.load(myfile)

    while True:
        spoken = input("You: ")
        spoken = spoken.lower()
        spoken = spoken.split(' ')
        prob = dict()

        for key, val in data[0]['question'].items():
            prob[key] = 0
            for j in spoken:
                if j in val:
                    prob[key]+=1
            prob[key] = (prob[key]/len(val))*(prob[key]/len(val))

        max = 0
        for k, v in prob.items():
            if v > max:
                max = v

        if max != 0:
            toprint = ''
            toprintList = list()
            for k, v in prob.items():
                if v == max:
                    toprint = k
                    toprintList.append(k)

            index = random.randint(0, len(toprintList)-1)
            toprint = toprintList[index]

        else:
            if 'default' in error:
                toprint = 'error'
            else:
                print(botName + ': ' + error)
                continue

        length = len(data[0]['answer'][toprint])
        num = random.randint(0,length-1)
        print(botName+' is typing ...')
        time.sleep(random.randint(0,3))
        print(botName+': '+data[0]['answer'][toprint][num])



def convert(person1, person2, txtFileName, jsonFileName):
    '''
    Description: Function that reads the raw txt file of the conversation and converts it to a json data file.
    Inputs :
        - person1: Specifies the name of the person who asks questions.
        - person2: Specifies the name of the person who answers, the person who will be the bot.
        - txtFileName: Specifies the name of the txt file containing the raw conversation.
        - jsonFileName: Specifies the name of the json file in which the conversation will be formatted.
    '''
    with open(txtFileName, 'r') as f:
        raw_data = f.readlines()

    with open (jsonFileName) as myfile:
        data = json.load(myfile)

    raw_data_2 = []
    storedAnswer = ''
    storedQuestion = ''
    answerString = ''
    questionString = ''
    question = False
    answer = False
    skip=False
    for i in range(len(raw_data)):
        if question:
            questionString += raw_data[i]
        if answer:
            answerString += raw_data[i]
        if person1 in raw_data[i]:
            question = True
            answer = False
            questionString = ''

        if question is True and person2 in raw_data[i+1]:
            storedQuestion  = questionString
            question = False

        if person2 in raw_data[i]:
            answer = True
            answerString = ''

        if answer is True and person1 in raw_data[i+1]:
            storedAnswer = answerString
            storedAnswer = storedAnswer.lower().replace('\t', ' ')
            storedAnswer = storedAnswer.replace('\n', ' ')
            storedQuestion = storedQuestion.lower().replace('\t', ' ')
            storedQuestion = storedQuestion.replace('\n', ' ')
            answer = False
            name = 'question' + str(data[1])
            data[1] += 1
            data[0]['question'][name] = storedQuestion.split(' ')
            data[0]['answer'][name] = [storedAnswer]
            print(storedQuestion)
            with open(jsonFileName, "w") as myfile:
                json.dump(data, myfile, indent=4)

if __name__ == '__main__':
    if input('convert?')=='y':
        convert('Gouin', 'John', 'data_john_raw.txt', 'data_john.json')

    ai('data_john.json', 'John', 'I dont know')