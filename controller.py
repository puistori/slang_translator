from flask import Flask, render_template, request, redirect , jsonify, json, Response, url_for, send_file
from jinja2 import Template
import sys
sys.path.insert(1, 'core_files/Finnish Slang/')
from finnish_translator import *
#from sumfin import sheppy
import re



#from core_files.Finnish Slang. import translate_finnish
# !!! oiko gives aa ... :(
app = Flask(__name__)

# This is a provisional database of acceptable email-password combos.
# Random TODO list: prettify , testing

## hmm, am I allowed to put it here?
file = open("core_files/Finnish Slang/assign1.3_out","rb")
sanalista = pickle.load(file)
file.close()

med = {}

for fru in sanalista:
    med.update(fru)

for old_key in med:
    new_key = old_key.lower()
    med[new_key] = med.pop(old_key)


@app.route("/main")
def main():
    return render_template('main.html')

@app.route("/css")
def css():
    return send_file("resources/main.css")

@app.route("/translate")
def translate():
    text = request.args.get('input',"",type=str)
    text = clean_up_input(text)
    print("string?")
    print(text)
    
    answer = translate_finnish(text,med)
    answer = str(answer)
    print('kester')
    print(answer)
    print('kester')
    return jsonify(result=(answer))
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
    return render_template('index.html')

@app.route('/introENG',methods=['POST'])
def intro_eng():
    # I'm not closing any of these files . . . is that a problem?
    intro = ""
    file = open('text/intro.txt','rt').readlines()
    for line in file:
        intro += line
    

    p2 = ""
    file = open('text/p2_eng.txt','rt').readlines()
    for line in file:
        p2 += line
    

    p3 = ""
    file = open('text/p3_eng.txt','rt').readlines()
    for line in file:
        p3 += line
    

    p4 = ""
    file = open('text/p4_eng.txt','rt').readlines()
    for line in file:
        p4 += line
    

    p5 = ""
    file = open('text/p5_eng.txt','rt').readlines()
    for line in file:
        p5 += line
    

    headers = []
    file = open('text/headers_eng.txt','rt').readlines()
    for line in file:
        headers.append(line)
    
    return (jsonify(intro=intro,p2=p2,p3=p3,p4=p4,p5=p5,headers=headers))



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

    return html_input


if __name__ == '__main__':
 app.run(debug=True)

