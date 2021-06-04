import re
def merge_reports(reports_num, path = './reports/'):
    reports = list()
    for i in range(reports_num):
        i = i + 1
        if i not in [40, 47, 112]:
            filename = path + 'report' + str(i) + '.txt'
            f = open(filename, 'r')
            reports.append(f.readlines()[0])
            f.close()
    filename = path + 'merged_reports.txt'
    f = open(filename, 'w')
    for item in reports:
        f.write(item + '\n')
    f.close()
    return reports

def merge_publications(publications_num, path = './publications/'):
    publications = list()
    for i in range(publications_num):
        i = i + 1
        if i not in [40, 47, 112]:
            filename = path + 'publication' + str(i) + '.txt'
            f = open(filename, 'r')
            content = f.readlines()[0]
            if content in publications:
                content = str(publications.index(content) + 1)
            #if content not in publications:
                #publications.append(content)
            #else:
                #publications.append(str(publications.index(content) + 1))
            f.close()
        else:
            content = 'null'
        publications.append(content)

    filename = path + 'merged_publications.txt'
    f = open(filename, 'w')
    for i, item in enumerate(publications):
        f.write(str(i + 1) + '\n')
        f.write(item + '\n')
    f.close()
    return publications

def load_phrases(path='./frequent_phrases.txt'):
    f = open(path, 'r')
    frequent_phrases = list()
    for line in f:
        frequent_phrases.append(line[line.index('\'')+1:line.rindex('\'')])
    return frequent_phrases

def load_topics(topics_num, path = './'):
    topics_phrases = list()
    fw = open('./merge_topic.txt', 'w')
    for i in range(topics_num):
        fw.write(str(i) + '\n')
        filename = path + 'topic' + str(i) + '.txt'
        #print(filename)
        f = open(filename, 'r')
        phrases = list()
        for line in f:
            phrases.append(line[0:line.rindex(' ')])
            fw.write(line[0:line.rindex(' ')] + '\n')
        f.close()
        topics_phrases.append(phrases)
    fw.close()
    return topics_phrases

def load_docs(path = './'):
    filename = path + 'publication_abstract.txt'
    f= open(filename, 'r')
    docs = list()
    for i, line in enumerate(f):
        if i%3 is 0:
            docs.append(line)
        elif i%3 is 1:
            docs[-1] = docs[-1] + line
    f.close()
    return docs
def refine_text():
    docs = load_docs()
    bracket_reg = r'(\([^()]*\))'
    bracket_re = re.compile(bracket_reg)
    #bracket_content = re.findall(abstract_re, html)
    for i, doc in enumerate(docs):
        bracket_content = re.findall(bracket_re, doc)
        if len(bracket_content) > 1:
            print(str(i) + '\t' + doc.split('\n')[0])
            print(bracket_content)
def write_input(path = './'):
    docs = load_docs()
    filename = path + 'nanotext.txt'
    f = open(filename, 'w')
    for doc in docs:
        f.write(doc)
    f.close()
def write_lattice(path = './'):
    filename = path + 'latice_output.txt'
    f = open(filename, 'w')
    for doc in docs:
        f.write(doc)
    f.close()
#merge_reports(120)
#merge_publications(120)
#load_docs()
#refine_text()
#write_input()
