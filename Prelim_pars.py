from flask import Flask
app = Flask(__name__)

@app.route('/pars/<string:file>')

def quizzer_pars(file):
    import string
    reference = set(string.punctuation)
    import os
    import scipy
    article = open(str(file), 'r')
    long_art_string= article.read()
    no_newline = long_art_string.replace("\n", " ")
    if "!" in no_newline:
        no_sent_punct = no_newline.split("!")
        for elem in no_sent_punct:
            if "." in elem:
                sam = elem.split(".")
                no_sent_punct.remove(elem)
                no_sent_punct.append(sam)
    else:
        no_sent_punct = no_newline.split(".")
    ultimatum ={}
    for phrase in no_sent_punct:
        if "?" in phrase:
            medium = phrase.slice("?")
            pos_ques = medium[0]
            medium = medium.remove(pos_ques)
            ultimatum[pos_ques] = str(medium)
        else:
            ultimatum[phrase] = 'determination'
    return str(ultimatum)
