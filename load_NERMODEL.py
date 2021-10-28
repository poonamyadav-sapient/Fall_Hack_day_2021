import spacy
from getReceiptText import GetReceiptText

class loadNERmodel():
    nlp=spacy.load('/Users/poonam.yadav/Desktop/FallHackday2021_Project/Fall_Hack_day_2021/output/model-best')
    receipt_no, item_texts, summary_texts = GetReceiptText().getText()
    doc1=nlp(item_texts[5])
    doc2 = nlp(summary_texts[5])
    print("---------------Entity Label for Receipt:{0}-----------".format(receipt_no[5]))
    print("---------ITEM ENTITY LABEL---------------------\n")
    for ent in doc1.ents:
        print("entity->{0} and label->{1}".format(ent, ent.label_))

    print("---------SUMMARY ENTITY LABEL---------------------\n")
    for ent in doc2.ents:
        print("entity->{0} and label->{1}".format(ent, ent.label_))


loadNERmodel()