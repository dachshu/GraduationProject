import json

def process_sentence(sentence):
    sentence = sentence.replace('\n', ' ')
    i = 0
    while True:
        if((sentence[i] < '가' or sentence[i] > '힣') and sentence[i] != ' '):
            if(i > 0 and sentence[i - 1] != ' '):
                sentence = sentence[:i] + ' ' + sentence[i:]
                i = i + 1
            if(i < len(sentence) - 1 and sentence[i + 1] != ' '):
                sentence = sentence[:i + 1] + ' ' + sentence[i + 1:]
                i = i + 1
        i = i + 1
        if(i == len(sentence)): break
    if(sentence[-1] != ' '): sentence = sentence + ' '
    sentence = sentence + '\n'
    return sentence

def process_data(file_name):
    f = open(file_name, encoding='UTF8')
    data_list = json.loads(f.read())
    
    titles = []
    comments = []
    vocab = set()
    
    word_train_text =  open('word_train.txt', 'w', encoding='UTF8')
    char_rnn_train_data = open('char_rnn_data.txt', 'w', encoding='UTF8')
    for data in data_list:
        title = process_sentence(data["title"])
        word_train_text.write(title)
        vocab.update(title.split(' '))
        i = 1
        for comment in data["comments"]:
            cmt = process_sentence(comment)
            vocab.update(cmt.split())
            comments.append(cmt)
            word_train_text.write(cmt)
            title = title.replace('\t', ' ')
            char_rnn_train_data.write(title.replace('\n', '') + '\t' +  cmt)

            #vocab.add(str(i))
            #t = str(i) + ' ' + title
            t = title
            titles.append(t)

            i = i + 1
    f.close()
    word_train_text.close()
    char_rnn_train_data.close()
    title_file = open('title.txt', 'w', encoding='UTF8')
    for title in titles:
        title_file.write(title)
    title_file.close()

    comment_file = open('comment.txt', 'w', encoding='UTF8')
    for comment in comments:
        comment_file.write(comment)
    comment_file.close()

    vocab_file = open('vocab.txt', 'w', encoding='UTF8')
    vocab_file.write('<unk>\n')
    vocab_file.write('<s>\n')
    vocab_file.write('</s>\n')
    for voca in vocab:
        voca = voca + '\n'
        vocab_file.write(voca)
    vocab_file.close()

process_data('./output/output.json')
