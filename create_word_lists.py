import nltk
import wordfreq

word_list = list(set([word for word in nltk.corpus.words.words() if word.islower()]))
common_words = [word for word in word_list if wordfreq.zipf_frequency(word, 'en') > 4]

def create_word_list(pos):

    pos_tag = ''
    if pos == 'noun':
        pos_tag = 'NN'
    if pos == 'pl-noun':
        pos_tag = 'NNS'
    if pos == 'verb':
        pos_tag = 'VB'
    if pos == 'adj':
        pos_tag = 'JJ'

    filtered_words = [word for word in common_words if nltk.pos_tag([word])[0][1] == pos_tag] #1st item (pos) of the 0th word

    with open(f'{pos}.txt', 'w') as f:
        for word in filtered_words:
            f.write(word + "\n")

create_word_list('adj')
create_word_list('verb')
create_word_list('pl-noun')
create_word_list('noun')
