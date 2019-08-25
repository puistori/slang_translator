from flask import Flask, render_template, request, redirect , jsonify, json, Response, url_for, send_file
from jinja2 import Template
import sys
sys.path.insert(1, 'core_files/Finnish Slang/')
from finnish_translator import *
#from sumfin import sheppy
import re
from pymongo import MongoClient 


#from core_files.Finnish Slang. import translate_finnish
# !!! oiko gives aa ... :(
app = Flask(__name__)

# This is a provisional database of acceptable email-password combos.
# Random TODO list: prettify , testing

# All of these are for finding manyword entries.
group1 = pickle.load(open('manyworded_entries/manyword_entries_g1','rb'))
group1_second_members = pickle.load(open('manyworded_entries/manyword_entries_g1_second_pair_members','rb'))
group1_verbs = pickle.load(open('manyworded_entries/manyword_entries_g1_verbs','rb'))

group2 = pickle.load(open('manyworded_entries/manyword_entries_g2','rb'))
#!!! this should be a dictionary.
group2_last_words = pickle.load(open('manyworded_entries/manyword_entries_g2_last_words','rb'))

group3 = pickle.load(open('manyworded_entries/manyword_entries_g3','rb'))
group3_layer_2 = pickle.load(open('manyworded_entries/manyword_entries_g3_layer_2','rb'))

group4 = pickle.load(open('manyworded_entries/manyword_entries_g4','rb'))
#!!! this shoudl be a dictionary.
group4_last_words = pickle.load(open('manyworded_entries/manyword_entries_g4_last_words','rb'))

manyword_stem_database = [group1,group1_second_members,group1_verbs,group2,group2_last_words,group3,group3_layer_2,group4,group4_last_words]






## hmm, am I allowed to put it here?
file = open("resources/slang_database","rb")
sanalista = pickle.load(file)
file.close()
print("going ghost")
print(type(sanalista))
print(sanalista[list(sanalista.keys())[0]])
print("done lol")

med = sanalista

for old_key in med:
    new_key = old_key.lower()
    med[new_key] = med.pop(old_key)

# Hardcoded fixes - words to be ignored.
ignore_us_file = open("resources/ignore_us.txt",'rt')
ignore_us = set([])
whitespace_ig = set([' ','','\n'])
for line in ignore_us_file.readlines():
        for entry in line.split(','):
                if entry not in whitespace_ig:
                        ignore_us.add(entry)

exact_matches_file = open("resources/exact_matches",'rb')
exact_matches = pickle.load(exact_matches_file)


@app.route("/main/eng")
def main_eng():
    return render_template('main.html',lang_code="eng")
@app.route("/main/sve")
def main_sve():
    return render_template('main.html',lang_code="sve")
@app.route("/main/suo")
def main_suo():
    return render_template('main.html',lang_code="suo")


@app.route("/main/css")
def css():
    return send_file("resources/main.css")





import sys 
@app.route("/translate")
def translate():
    text = request.args.get('input',"",type=str)
    print("no?")
    print("\n\n\n\n")
    print(text)
    text = clean_up_input(text)
    print("string?")
    print("\n\n\n")
    print(text)
    sys.stdout.flush()
    
    
    answer = translate_finnish(text,med,manyword_stem_database,exact_matches=exact_matches,ignore_us=ignore_us)
    answer = str(answer)
    print('kester')
    print(answer)
    print('kester')
    return jsonify(result=(answer),cleaned_text=(text))
    #return jsonify(result=text)


@app.route("/test")
def test():
    return render_template('testing.html')

@app.route("/pull",methods=['POST'])
def pull():    
    return render_template('pull.html')

@app.route("/jquery")
def consent():
    return send_file("resources/jquery.js")

@app.route('/_add_numbers')
def add_numbers():
    a = request.args.get('a', 0, type=int)
    b = request.args.get('b', 0, type=int)
    print(sheppy(a,b))
    return jsonify(result= (sheppy(a,b)))

@app.route('/')
def index():
    return redirect(url_for('main_eng'))


@app.route('/ENG',methods=['POST'])
def intro_eng():
    # I'm not closing any of these files . . . is that a problem?
    intro = ""
    file = open('text/eng/intro.txt','rt',encoding='utf8').readlines()
    for line in file:
        intro += line
    

    p2 = ""
    file = open('text/eng/p2.txt','rt',encoding='utf8').readlines()
    for line in file:
        p2 += line
    

    p3 = ""
    file = open('text/eng/p3.txt','rt',encoding='utf8').readlines()
    for line in file:
        p3 += line
    

    p4 = ""
    file = open('text/eng/p4.txt','rt',encoding='utf8').readlines()
    for line in file:
        p4 += line

    updated = ""
    file = open('text/eng/updated.txt','rt',encoding='utf8').readlines()
    for line in file:
        updated += line

    p5 = ""
    file = open('text/eng/p5.txt','rt',encoding='utf8').readlines()
    for line in file:
        p5 += line

    p6 = ""
    file = open('text/eng/p6.txt','rt',encoding='utf8').readlines()
    for line in file:
        p6 += line
    

    headers = []
    file = open('text/eng/headers.txt','rt',encoding='utf8').readlines()
    for line in file:
        headers.append(line)
    labels = []
    file = open('text/eng/labels.txt','rt',encoding='utf8').readlines()
    for line in file:
        labels.append(line)
    
    return (jsonify(intro=intro,p2=p2,p3=p3,p4=p4,p5=p5,p6=p6,headers=headers,labels=labels,updated=updated))

@app.route('/SVE',methods=['POST','GET'])
def intro_sve():
    # I'm not closing any of these files . . . is that a problem?
    intro = ""
    file = open('text/sve/intro.txt','rt',encoding='utf8').readlines()
    for line in file:
        intro += line
    

    p2 = ""
    file = open('text/sve/p2.txt','rt',encoding='utf8').readlines()
    for line in file:
        p2 += line
    

    p3 = ""
    file = open('text/sve/p3.txt','rt',encoding='utf8').readlines()
    for line in file:
        p3 += line
    

    p4 = ""
    file = open('text/sve/p4.txt','rt',encoding='utf8').readlines()
    for line in file:
        p4 += line

    updated = ""
    file = open('text/sve/updated.txt','rt',encoding='utf8').readlines()
    for line in file:
        updated += line    

    p5 = ""
    file = open('text/sve/p5.txt','rt',encoding='utf8').readlines()
    for line in file:
        p5 += line

    p6 = ""
    file = open('text/sve/p6.txt','rt',encoding='utf8').readlines()
    for line in file:
        p6 += line
    

    headers = []
    file = open('text/sve/headers.txt','rt',encoding='utf8').readlines()
    for line in file:
        headers.append(line)

    labels = []
    file = open('text/sve/labels.txt','rt',encoding='utf8').readlines()
    for line in file:
        labels.append(line)

    return (jsonify(intro=intro,p2=p2,p3=p3,p4=p4,p5=p5,p6=p6,headers=headers,labels=labels,updated=updated))

@app.route('/SUO',methods=['POST','GET'])
def intro_suo():
    # I'm not closing any of these files . . . is that a problem?
    intro = ""
    file = open('text/suo/intro.txt','rt',encoding='utf8').readlines()
    for line in file:
        intro += line
    

    p2 = ""
    file = open('text/suo/p2.txt','rt',encoding='utf8').readlines()
    for line in file:
        p2 += line
    

    p3 = ""
    file = open('text/suo/p3.txt','rt',encoding='utf8').readlines()
    for line in file:
        p3 += line
    

    p4 = ""
    file = open('text/suo/p4.txt','rt',encoding='utf8').readlines()
    for line in file:
        p4 += line
    
    updated = ""
    file = open('text/suo/updated.txt','rt',encoding='utf8').readlines()
    for line in file:
        updated += line

    p5 = ""
    file = open('text/suo/p5.txt','rt',encoding='utf8').readlines()
    for line in file:
        p5 += line

    p6 = ""
    file = open('text/suo/p6.txt','rt',encoding='utf8').readlines()
    for line in file:
        p6 += line
    

    headers = []
    file = open('text/suo/headers.txt','rt',encoding='utf8').readlines()
    for line in file:
        headers.append(line)

    labels = []
    file = open('text/suo/labels.txt','rt',encoding='utf8').readlines()
    for line in file:
        labels.append(line)

    return (jsonify(intro=intro,p2=p2,p3=p3,p4=p4,p5=p5,p6=p6,headers=headers,labels=labels,updated=updated))

@app.route("/report")
def misslematizations():
    
    lemma= request.args.get('lemma', "no lemma", type=str)
    instance = request.args.get('instance','no instance',type=str)

    print("on wi go!")
    print(request.args)
    print(lemma)

    mongo_client = MongoClient("mongodb+srv://puistori:gebit%40worker92@incidental-acquisition-caxuy.mongodb.net/test?retryWrites=true&w=majority")
    db = mongo_client.SlangTranslator.wrong_lemmatizations
    insert_this = {lemma:instance}
    db.insert_one(insert_this)
    
    return('boo')


#everything down here is just me goofing around as I learn
@app.route("/floop")
def floop():
    lurst = []
    for number in range(4):
        lurst.append(number)
       
    return (str(lurst))

#@app.route('/flarp')
#def index():
# return render_template('index.html',something = "joana bidiana")

@app.route('/response', methods=['POST'])
def nupperino():
    return render_template('response.html', klop = request.form.get('firstname'), klasp = request.form.get('lastname') )



### Helper methods

"""
valid_email() method. 
This method checks the validity of an input.
It is by no means exhaustive, and is more than likely 
not necessary in the final version. 

"""


def report_misslematization(lemma,instance):
        mongo_client = MongoClient("mongodb+srv://puistori:gebit%40worker92@incidental-acquisition-caxuy.mongodb.net/test?retryWrites=true&w=majority")
        db = mongo_client.SlangTranslator.wrong_lemmatizations
        insert_this = {lemma:instance}
        db.insert_one(insert_this)

def valid_email(email):
    # Checking if it's long enough. There's no valid email shorter than 6
    if len(email) >5:
        # Checking if it has a valid ending
        if email[len(email)-4:] in ['.com','.net','.org','.gov']:
            # Checking if it has an '@' character in it, and that it doesn't begin with it.
            if "@" in email[:-4] and email[0] != "@":
                # return True if all of these conditions were met.
                return True
    # Return False otherwise.
    return False 

# This is very sloppily done, sorry. but basically, all of the extra HTML that gets inserted in order for me to have the highlighting and the tooltip
# basically will end up being part of the input for the translation function. We gotta get rid of it so that we're dealing with just good old normal text.
def clean_up_input(html_input):

    # All of these replacements were motivated by dealing with HTML code that was injected 
    # by my own application, when it tried to make tooltips and stuff. 
    # "<div class='tooltip' name='$' readonly><mark>$</mark><span class='tooltiptext'>$</span></div>";
    html_input = html_input.replace('<div class=\"tooltip\" name=\"','')
    html_input = html_input.replace("\" readonly><mark>$</mark><span class=\"tooltiptext\">$</span></div>", '')
    html_input = re.sub(r"\" readonly=\"\"><mark>.*?<\/mark><span class=\"tooltiptext\">.*?'</span>", '', html_input)
    html_input = re.sub(r"div class='tooltip'","",html_input)
    html_input = re.sub(r"<span class='tooltiptext'>.*?</span>","",html_input)
    html_input = html_input.replace("&nbsp;","")
    html_input = html_input.replace("<div>","")
    html_input= html_input.replace("</div>","")
    html_input= html_input.replace("<br>","")
    html_input = html_input.replace('<span style="background-color: rgb(255, 255, 0);">','')
    html_input = html_input.replace('</span>','')

    #These replacements are motivated by dealing with HTML code that got copy and pasted in from other websites
    #genius.com
    html_input = re.sub(r"<span style=.*?>","",html_input)
    html_input = re.sub(r"<br style=.*?>","\n",html_input)
    return html_input


print("Mick mulvaney is lame")

unser = translate_finnish("euforia on paras juttu, ja totta, bongi muna",med,manyword_stem_database)

for blip in unser:
    print('a1 steak sauce')
    print(blip)


if __name__ == '__main__':
 app.run(debug=True)

