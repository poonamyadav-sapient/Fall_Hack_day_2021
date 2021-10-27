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
        patterns = {"item_rsd": r'[Total]?([\w\s\-\+]{5,64})\s\$',
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
            "item_rsd": re.compile(r"([\w\s\-\+]{5,64})\s\$")
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
        item_texts, summary_texts = GetReceiptText().getText()
        print(item_texts)
        for index,item_text in enumerate(item_texts):
            doc=self.create_item_entity(item_text)
            print("************************Receipt id-{0}********************".format(index))
            print("--------------entities----------------")
            for ent in doc.ents:
                if ent.label_ == "item_rsd":
                    ent = self.clean_data_matcher(ent.label_,ent.text)
                    print("ent",ent)
                    print("entity is:item name-{0}".format(ent))
                else:
                    print("ent",ent)
                    ent = self.clean_data_matcher(ent.label_,ent.text)
                    print("entity is:qty-{0} amount-{1}".format(ent[0], ent[1]))


if __name__ == "__main__":
    createNERdata().load_entity()