import os
import json
import string
import requests
import spacy
import json
from spacy.attrs import ENT_IOB, ENT_TYPE

from flask import Flask, Response
app = Flask(__name__)

#if call in server and entry comes up then print table
#else:
    #raws = url_for(local_host/ping/user_strg)
    #quest, ansr = url_for(local_host/pars/raws)
    #call data base and implement quest,ansr to user_strg keys, name object
    #return quiz cards or simple preset of questions

@app.route('/p/')
def parse():
    json_data = requests.get("https://tzylobx763.execute-api.us-east-1.amazonaws.com/dev/ping/Albert%20Einstein").content
    en_nlp = spacy.load('en')
    doc = en_nlp(json.loads(json_data)['query']['pages'][0]['extract'])
    res = ' '
    for sent in list(doc.sents):
        res = res + "{" + str(sent) + '}<br/> '
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
    api_url = 'https://en.wikipedia.org/w/api.php?action=query&prop=revisions&format=json&prop=extracts&&titles=' + article_name
    return requests.get(api_url).content

@app.route('/test-spacey/')
def test():
    en_nlp = spacy.load('en')
    doc = en_nlp(u'He gave up looking for fully generally covariant tensor equations, and searched for equations that would be invariant under general linear transformations only.')
    res = ''
    i = 0
    for val in doc:
        res = res + str(doc[i].text) + ', ' + str(doc[i].ent_iob) + ', ' + doc[i].ent_type_ + '\n'
        i += 1
    return res

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
