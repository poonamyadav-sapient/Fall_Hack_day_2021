import en_core_web_sm
import spacy
from spacy.tokens import span
from spacy.matcher import Matcher
from spacy.language import Language
import pandas as pd
import re
from getReceiptText import GetReceiptText
from spacy.tokens import DocBin

class createNERdata():

    @Language.component('clean_data_matcher')
    def clean_data_matcher(self,entity_label, doc):
        patterns = {"item_rsd": r'(?:Price Qty Total\s)?([\w\s\-\+\(\)\$\#\!\&]{5,64})\s\$',
                    "item_qty_amount": r'(\d{1,3})\s\$(\d{1,3}\.\d{2})',
                    "subtotal": r"Subtotal\:\s\$(\d{1,3}\.\d{2})",
                    "tax": r"Tax\:\s\$(\d{1,3}\.\d{2})",
                    "total": r"Total\:\s\$(\d{1,3}\.\d{2})"
                    }
        for pattern, expression in patterns.items():
            if entity_label == pattern:
                result = re.findall(expression, doc)
                # print("result",result)
        return result if result else None

    @Language.component('regex_matcher')
    def regex_matcher(doc):
        expressions = {
            "item_rsd": re.compile(r"([\w\s\-\+\(\#\!\&\)\$]{5,64})\s\$\d{1,3}\.\d{2}"),
            "item_qty_amount": re.compile(r"(\d{1,3})\s\$(\d{1,3}\.\d{2})"),
            "subtotal": re.compile(r"Subtotal\:\s\$(\d{1,3}\.\d{2})"),
            "tax": re.compile(r"Tax\:\s\$(\d{1,3}\.\d{2})"),
            "total": re.compile(r"Total\:\s\$(\d{1,3}\.\d{2})")
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


    def create_entity(self,item_text):
        nlp = spacy.load("en_core_web_lg", disable=['ner'])
        nlp.add_pipe('regex_matcher')
        doc = nlp(item_text)
        return doc

    def load_entity(self):
        receipt_no, item_texts, summary_texts = GetReceiptText().getText()
        db = DocBin()
        item_dict = {
            'Receipt': [],
            'Item_RSD': [],
            'Item_Qty': [],
            'Item_Price': []
        }
        summary_dict = {
            'Receipt': [],
            'Subtotal': [],
            'Tax': [],
            'Total': []
        }
        for i in range(len(item_texts)):
            doc=self.create_entity(item_texts[i])
            doc2=self.create_entity(summary_texts[i])
            db.add(doc)
            db.add(doc2)
            print("************************Receipt id-{0}********************".format(receipt_no[i]))
            print("--------------entities----------------")
            item_data = self.itemExtracter(doc, receipt_no[i])
            summary_data = self.summaryExtracter(doc2, receipt_no[i])

            item_dict['Receipt'] += item_data['Receipt']
            item_dict['Item_RSD'] += item_data['Item_RSD']
            item_dict['Item_Qty'] += item_data['Item_Qty']
            item_dict['Item_Price'] += item_data['Item_Price']

            summary_dict['Receipt'].append(summary_data['Receipt'][0])
            summary_dict['Subtotal'].append(summary_data['Subtotal'][0])
            summary_dict['Tax'].append(summary_data['Tax'][0])
            summary_dict['Total'].append(summary_data['Total'][0])

        self.uploadToCSV(item_dict, 'item')
        self.uploadToCSV(summary_dict, 'summary')


        db.to_disk("/Users/poonam.yadav/Desktop/FallHackday2021_Project/Fall_Hack_day_2021/data/training_data/train.spacy")

    def itemExtracter(self, doc, receipt_no):
        receipt_num = []
        item_rsd = []
        item_qty = []
        item_price = []

        for ent in doc.ents:
            # print("entity is {0} and label is {1}".format(ent, ent.label_))
            if ent.label_ == "item_rsd":
                abc = self.clean_data_matcher(ent.label_, ent.text)
                # print("ent", abc)
                print("\nentity is:item name-{0}".format(abc))
                receipt_num.append(receipt_no)
                item_rsd.append(abc[0])
            elif ent.label_ == "item_qty_amount":
                abc = self.clean_data_matcher(ent.label_, ent.text)
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
        return data

    def summaryExtracter(self, doc, receipt_no):
        receipt_num = []
        subtotal = []
        tax = []
        total = []

        receipt_num.append(receipt_no)
        for ent in doc.ents:
            # print("entity is {0} and label is {1}".format(ent, ent.label_))
            if ent.label_ == "subtotal":
                abc = self.clean_data_matcher(ent.label_, ent.text)
                # print("ent", abc)
                print("subtotal", abc[0])
                subtotal.append(abc[0])
                # try:
                #     print("entity is:qty-{0} amount-{1}".format(abc[0][0], abc[0][1]))
                # except:
                #     print("Failed")
            elif ent.label_ == "tax":
                abc = self.clean_data_matcher(ent.label_, ent.text)
                # print("ent", abc)
                print("tax", abc[0])
                tax.append(abc[0])
                # try:
                #     print("entity is:qty-{0} amount-{1}".format(abc[0][0], abc[0][1]))
                # except:
                #     print("Failed")
            elif ent.label_ == "total":
                abc = self.clean_data_matcher(ent.label_, ent.text)
                # print("ent", abc)
                print("total", abc[0])
                total.append(abc[0])
                # try:
                #     print("entity is:qty-{0} amount-{1}".format(abc[0][0], abc[0][1]))
                # except:
                #     print("Failed")

        data = {
            'Receipt': receipt_num,
            'Subtotal': subtotal,
            'Tax': tax,
            'Total': total
        }
        df = pd.DataFrame(data)
        df.to_csv("summary.csv", mode="w", index=False)
        return data

    def uploadToCSV(self, data, type):
        df = pd.DataFrame(data)
        if type == 'item':
            df.to_csv("items.csv", mode="w", index=False)
        elif type == 'summary':
            df.to_csv("summary.csv", mode="w", index=False)

if __name__ == "__main__":
    createNERdata().load_entity()