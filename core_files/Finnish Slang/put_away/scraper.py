import bs4
import urllib.request
import re
import csv




url_base = "https://urbaanisanakirja.com/search/?q="





def fetch_word_url(word):

    # you'll want this later
    possibly_related_words = []
    #  # #  # # # # # #

    domain_name = "https://urbaanisanakirja.com"

    word = word.lower()
    try:
        url = url_base+word
        source = urllib.request.urlopen(url).read()
        soup = bs4.BeautifulSoup(source,'lxml')
    except:
        print("Url not found, lol ")
        return(False)
    #print(type(soup))

    try:

        content = soup.find("div",id="content")
        rows = content.find_all("div",class_="row")

        # Ok, first we need to see if there are any entries for the word.
        sana_otsikossa = False
        for row in rows:
            h_three = row.find("h3")

            if h_three != None:
                h_three = h_three.text
                haku_tulos = re.search(r"Hakutulos joissa \".*\" otsikossa",h_three)
                if haku_tulos != None:
                    sana_otsikossa = True
    except:

        print("downstream problems fam :(")
        return(False)
    if sana_otsikossa:
        #print("Yes! there are entries!")
        # Ok, IF there is an entry, it will be in the second row tag, at index 1 of the rows object
        # which is just a list of rows.
        row_of_interest = rows[1]

        # That row is made up of columns. Each column has a table which contains all the words which have our sought-after
        # word in the title. Let's look through all of these tables, and return all of the links , and of course the word
        # itself. We can stop early if we get an exact match, and I'll do that with a 'break' call.

        columns = row_of_interest.find_all("div",class_="col-md-3")
        for column in columns:
            table = column.find("table",class_="table table-condensed table-striped")
            if table != None:
                #print(table)
                # Every table, which represents a colum in the larger scheme of things, is composed of tr tags,
                # and these tr tags contain the words themselves. Let's crack these open and add them to the
                # possibly related words list. That will only come in handy if we can't find the word we are looking
                # for, but if other entries exist.
                tr_tags = table.find_all("tr")
                for tr_tag in tr_tags:
                    td_tag = tr_tag.td
                    link = td_tag.a.get("href")
                    text = td_tag.text
                    # Ok , so , if you get an exact match, then you can quit.
                    text = text.lower()
                    text = re.sub(" ","",text)
                    if text == word:
                        desired_url = domain_name+link
                        return(desired_url)
                    else:
                        possibly_related_words.append(text)

            # an error message, just in case... this shouldn't ever happen though.
            else:
                print("A column had no table - for the word : %s"%word)
        return(possibly_related_words)


    else:
        print("No, there is no entry for this word :(")
        return(None)
    #print(content)


def fetch_definition(url):
    source = urllib.request.urlopen(url).read()
    soup = bs4.BeautifulSoup(source, 'lxml')
    content = soup.find("div", id="content")
    row = content.find("div",class_="row")
    answer_column = row.find("div",class_="col-md-6 col-md-push-3")

    answers = answer_column.find_all("div",class_="box-container")

    # ok, so all of those "box containers" are the grey boxes you see on the website that contain the various
    # proposed translations. For now, I'm only interested in the top one (the most well recieved translation)
    # so I will look only at the 0th index. Let's get this bread!
    if answers != None:
        top_answer = answers[0]
        top_answer_box = top_answer.find("div",class_="box")
        definition = top_answer_box.find("p")
        definition = definition.text
        definition = re.sub("(  )|(\n)","",definition)
        examples = top_answer.find("blockquote")
        examples = examples.text
        examples = re.sub("(  )|(\n)", "", examples)
        if examples == None:
            examples = " "
        if definition == None:
            definition = " "
        return(True,definition,examples)

    else:
        print("something went wrong :( ")
        return (False,None,None)

