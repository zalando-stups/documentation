#!/usr/bin/env python3

'''
make text
find _build/text/ -name '*.txt' | xargs cat > _build/words.txt
'''

from os import path
from wordcloud import WordCloud, STOPWORDS

d = path.dirname(__file__)

STOPWORDS.add('will')
STOPWORDS.add('example')

# Read the whole text.
text = open(path.join(d, '_build/words.txt'), encoding='utf-8').read()
wordcloud = WordCloud(width=1920, height=1080, max_words=200).generate(text)
wordcloud.to_file('word-cloud.png')
