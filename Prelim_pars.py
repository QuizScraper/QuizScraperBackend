# coding=utf-8

import os
import json
import string
import requests
import spacy
from flask import jsonify
from collections import OrderedDict

from flask import Flask, Response
app = Flask(__name__)

en_nlp = spacy.load('en')

#if call in server and entry comes up then print table
#else:
    #raws = url_for(local_host/ping/user_strg)
    #quest, ansr = url_for(local_host/pars/raws)
    #call data base and implement quest,ansr to user_strg keys, name object
    #return quiz cards or simple preset of questions

@app.route('/p/<article_name>')
def parse(article_name):
    parse_url = "http://ec2-52-206-34-202.compute-1.amazonaws.com:5000/ping/" + article_name
    data = requests.get(parse_url).content
    en_nlp = spacy.load('en')
    doc = en_nlp(unicode(''.join((c for c in data if ord(c) < 128))))
    res = ' '
    for sent in list(doc.sents):
        #res = res + "{" + str(sent) + '}<br/> '
        sentence_api_url = 'http://ec2-52-206-34-202.compute-1.amazonaws.com:5000/parse_sentence/' + str(sent)
        res = res + str(requests.get(sentence_api_url).content)
    return res


@app.route('/parse/<string:file>')
def quizzer_pars(file):
    reference = set(string.punctuation)
    long_art_string= file
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
            ultimatum[pos_ques] = medium.remove(pos_ques)
            #medium = medium.remove(pos_ques)
            #ultimatum[pos_ques] = str(medium)
        else:
            ultimatum[phrase] = 'determination'
    return str(ultimatum)

@app.route('/ping/<article_name>')
def ping(article_name):
    #api_url = 'https://en.wikipedia.org/w/api.php?action=parse&format=json&page=' + article_name + '&redirects=&prop=wikitext'
    api_url = 'https://en.wikipedia.org/w/api.php?action=query&prop=revisions&format=json&prop=extracts&&titles=' + str(article_name)
    req = json.loads(requests.get(api_url).content, object_pairs_hook=OrderedDict)
    first = next(iter(req['query']['pages'].values()))
    return first['extract']

@app.route('/parse_sentence/<sentence>')
def parse_sentence(sentence):
    string = str(sentence).decode('utf8', errors='replace')
    doc = en_nlp(unicode(''.join((c for c in string if ord(c) < 128))))
    res = 'Input sentence: ' + string + ' <br/><br/>'
    for i in range(0, len(list(doc))):
        res = res + "{" + str(doc[i].text) + ", " + str(en_nlp.vocab.strings[doc[i].tag]) + '} '
    #res = res + str(doc[i].text) + ', ' + str(doc[i].ent_iob) + ', ' + doc[i].ent_type_ + '\n'

    if(str(en_nlp.vocab.strings[doc[0].tag]) == "NNP"):
        if(str(en_nlp.vocab.strings[doc[1].tag]) == "NNP"):
            if(str(en_nlp.vocab.strings[doc[2].tag]) == "VBD"):
                res = res + "<br /> <br /> Who "
                if(str(doc[len(list(doc))-1]) == '.'):
                    for i in range(2, len(list(doc))-1):
                        res = res + str(doc[i].text) + " "
                else:
                    for i in range(2, len(list(doc))):
                        res = res + str(doc[i].text) + " "
                res = res + "?" + " Answer: " + str(doc[0].text) + " " + str(doc[1].text)
        else:
            '''
            if(str(en_nlp.vocab.strings[doc[1].tag]) == "VBD"):
                res = res + "<br /> <br /> Who "
                if(str(doc[len(list(doc))-1]) == '.'):
                    for i in range(1, len(list(doc))-1):
                        res = res + str(doc[i].text) + " "
                else:
                    for i in range(1, len(list(doc))):
                        res = res + str(doc[i].text) + " "
                res = res + "?" + " Answer: " + str(doc[0].text)
            '''
    elif(str(en_nlp.vocab.strings[doc[0].tag]) == "IN"):
        if(str(en_nlp.vocab.strings[doc[1].tag]) == "CD"):
            if((str(en_nlp.vocab.strings[doc[3].tag]) == "NNP") and (str(en_nlp.vocab.strings[doc[4].tag]) == "NNP")):
                if((str(en_nlp.vocab.strings[doc[5].tag]) == "VBD")):
                    res = res + "<br /> <br /> When did " + str(doc[3].text) + " " + str(doc[4].text) + " " + str(doc[5].text)[0:len(str(doc[5].text))-1] + " "
                    if(str(doc[len(list(doc))-1]) == '.'):
                        for i in range(6, len(list(doc))-1):
                            res = res + str(doc[i].text) + " "
                    else:
                        for i in range(6, len(list(doc))):
                            res = res + str(doc[i].text) + " "
                    res = res + "?" + " Answer: " + str(doc[1].text)
        elif(str(en_nlp.vocab.strings[doc[1].tag]) == "NNP"):
            if(str(en_nlp.vocab.strings[doc[2].tag]) == "CD"):
                if((str(en_nlp.vocab.strings[doc[4].tag]) == "NNP") and (str(en_nlp.vocab.strings[doc[5].tag]) == "NNP")):
                    if((str(en_nlp.vocab.strings[doc[6].tag]) == "VBD")):
                        res = res + "<br /> <br /> When did " + str(doc[4].text) + " " + str(doc[5].text) + " " + str(doc[6].text)[0:len(str(doc[6].text))-1] + " "
                        if(str(doc[len(list(doc))-1]) == '.'):
                            for i in range(7, len(list(doc))-1):
                                res = res + str(doc[i].text) + " "
                        else:
                            for i in range(7, len(list(doc))):
                                res = res + str(doc[i].text) + " "
                        res = res + "?" + " Answer: In " + str(doc[1].text) + " " + str(doc[2].text)

    return res

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
