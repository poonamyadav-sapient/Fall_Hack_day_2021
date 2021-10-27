import en_core_web_sm
import spacy
from spacy.tokens import span
from spacy.matcher import Matcher
from spacy.language import Language
import pandas as pd
import re
from getReceiptText import GetReceiptText

class createNERdata():

    @Language.component('clean_data_matcher')
    def clean_data_matcher(self,entity_label, doc):
        patterns = {"item_rsd": r'(?:Price Qty Total\s)?([\w\s\-\+\(\)\$]{5,64})\s\$',
                    "item_qty_amount": r'(\d{1,3})\s\$(\d{1,3}\.\d{2})'
                    }
        for pattern, expression in patterns.items():
            if entity_label == pattern:
                result = re.findall(expression, doc)
                print("result",result)
        return result if result else None

    @Language.component('item_regex_matcher')
    def item_regex_matcher(doc):
        expressions = {
            "item_qty_amount": re.compile(r"(\d{1,3})\s\$(\d{1,3}\.\d{2})"),
            "item_rsd": re.compile(r"([\w\s\-\+\(\)\$]{5,64})\s\$\d{1,3}\.\d{2}")
        }
        spans = []
        for labels, expression in expressions.items():
            for match in re.finditer(expression, doc.text):
                start, end = match.span()
                entity = doc.char_span(start, end, label=labels, alignment_mode='contract')
                if entity:
                    spans.append(entity)
        doc.ents = list(doc.ents) + spacy.util.filter_spans(spans)
        return doc


    def create_item_entity(self,item_text):
        nlp = spacy.load("en_core_web_lg", disable=['ner'])
        nlp.add_pipe('item_regex_matcher')
        doc = nlp(item_text)
        return doc

    def load_entity(self):
        receipt_no, item_texts, summary_texts = GetReceiptText().getText()

        receipt_num = []
        item_rsd = []
        item_qty = []
        item_price = []
        for i in range(len(item_texts)):
            doc=self.create_item_entity(item_texts[i])
            print("************************Receipt id-{0}********************".format(receipt_no[i]))
            print("--------------entities----------------")
            for ent in doc.ents:
                # print("entity is {0} and label is {1}".format(ent, ent.label_))
                if ent.label_ == "item_rsd":
                    abc = self.clean_data_matcher(ent.label_,ent.text)
                    # print("ent", abc)
                    print("\nentity is:item name-{0}".format(abc))
                    receipt_num.append(receipt_no[i])
                    item_rsd.append(abc[0])
                else:
                    abc = self.clean_data_matcher(ent.label_,ent.text)
                    # print("ent", abc)
                    item_qty.append(abc[0][0])
                    item_price.append(abc[0][1])
                    try:
                        print("entity is:qty-{0} amount-{1}".format(abc[0][0], abc[0][1]))
                    except:
                        print("Failed")
        data = {
            'Receipt': receipt_num,
            'Item_RSD': item_rsd,
            'Item_Qty': item_qty,
            'Item_Price': item_price
        }
        print(data)
        print("receipt_num:", len(receipt_num))
        print("item_rsd:", len(item_rsd))
        print("item_qty:", len(item_qty))
        print("item_price:", len(item_price))
        df = pd.DataFrame(data)
        df.to_csv("values.csv", mode="w", index=False)

if __name__ == "__main__":
    createNERdata().load_entity()