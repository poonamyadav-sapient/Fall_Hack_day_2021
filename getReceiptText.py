import pandas as pd


class GetReceiptText:

    def getText(self):
        df = pd.read_csv('dataset.csv')
        item_text = df['Item_Text']
        summary_text = df['Summary_Text']

        return item_text, summary_text

