# import spacy
# from bs4 import BeautifulSoup
# import nltk
# import pandas as pd
# nltk.download('averaged_perceptron_tagger')
#
# from nltk.tokenize import word_tokenize, sent_tokenize
# from sklearn.feature_extraction.text import CountVectorizer
# from nltk.tokenize import RegexpTokenizer
#
# html = open('testingdata.html')
# soup = BeautifulSoup(html, features="html.parser")
# text = soup.get_text()
# # break into lines and remove leading and trailing space on each
# lines = (line.strip() for line in text.splitlines())
# # break multi-headlines into a line each
# chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
# # drop blank lines
# text = '\n'.join(chunk for chunk in chunks if chunk)
# file = open('read.txt', 'w')
# file.write(text)
# file.close()
# with open('read.txt','r') as f:
#     data = [line for line in f.readlines()]
#     print("data is",data)
# df = pd.DataFrame(data, columns=['text'])
# df.head()




import pandas as pd
import re
import os
from bs4 import BeautifulSoup
#
# html = open('html_files/135403722')
# soup = BeautifulSoup(html, features="html.parser")
# text = soup.get_text()
# # break into lines and remove leading and trailing space on each
# lines = (line.strip() for line in text.splitlines())
# # break multi-headlines into a line each
# chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
# # drop blank lines
# text = '\n'.join(chunk for chunk in chunks if chunk)
# item_pattern = re.compile(r'Item\(s\) In Your Order')
# summary_pattern = re.compile(r'Payment Information')
# summary_end_pattern = re.compile(r'Shipping & Billing')
#
#
# item_start_count = 0
# item_end_count = 0
# summary_start_count = 0
# summary_end_count = 0
#
# counter = 0
# text = text.splitlines()
# for lines in text:
#     if re.search(item_pattern, lines):
#         item_start_count = counter + 1
#
#     if re.search(summary_pattern, lines):
#         item_end_count = counter
#         summary_start_count = counter + 1
#
#     if re.search(summary_end_pattern, lines):
#         summary_end_count = counter
#
#     counter += 1
#
# item_lines = ' '.join(text[item_start_count:item_end_count])
# summary_lines = ' '.join(text[summary_start_count:summary_end_count])
#
# dict = {'Item_Text': str(item_lines), 'Summary_Text': str(summary_lines)}
# df = pd.DataFrame(dict)
# df.to_csv("dataset.csv", "a", index=False)

class CreateDataset:
    def __init__(self):
        dict = self.getText()
        self.uploadToCSV(dict)

    def getText(self):
        path = 'html_files/'

        item_lines = []
        summary_lines = []

        for receipts in os.listdir(path):
            html = open(path + receipts)
            print("\n\nCleaning Receipt:", receipts)
            text = self.cleanText(html)

            item_pattern = re.compile(r'Item\(s\) In Your Order')
            summary_pattern = re.compile(r'Payment Information')
            summary_end_pattern = re.compile(r'Shipping & Billing')

            item_start_count = 0
            item_end_count = 0
            summary_start_count = 0
            summary_end_count = 0

            counter = 0
            text = text.splitlines()
            for lines in text:
                if re.search(item_pattern, lines):
                    item_start_count = counter + 1

                if re.search(summary_pattern, lines):
                    item_end_count = counter
                    summary_start_count = counter + 1

                if re.search(summary_end_pattern, lines):
                    summary_end_count = counter

                counter += 1

            print("\nAdding receipt {} to dataset.".format(receipts))
            item_lines.append(' '.join(text[item_start_count:item_end_count]))
            summary_lines.append(' '.join(text[summary_start_count:summary_end_count]))

        dict = {'Item_Text': item_lines,
                'Summary_Text': summary_lines
                }
        print(dict)
        return dict

    def cleanText(self, html):
        soup = BeautifulSoup(html, features="html.parser")
        text = soup.get_text()
        # break into lines and remove leading and trailing space on each
        lines = (line.strip() for line in text.splitlines())
        # break multi-headlines into a line each
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        # drop blank lines
        text = '\n'.join(chunk for chunk in chunks if chunk)

        return text

    def uploadToCSV(self, dict):
        df = pd.DataFrame.from_dict(dict)
        df.to_csv("dataset.csv", "a", index=False)
        print("\n\n\n\nDataset created\n\n")

CreateDataset()