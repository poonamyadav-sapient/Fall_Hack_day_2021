import spacy
from getReceiptText import GetReceiptText

class loadNERmodel():
    nlp=spacy.load('/Users/poonam.yadav/Desktop/FallHackday2021_Project/Fall_Hack_day_2021/output/model-last')
    receipt_no, item_texts, summary_texts = GetReceiptText().getText()
    doc=nlp(item_texts[0])
    for ent in doc.ents:
        print("entity is{0} and entitylabel is {1}".format(ent, ent.label_))

loadNERmodel()