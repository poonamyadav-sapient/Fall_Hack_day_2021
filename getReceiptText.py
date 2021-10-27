import pandas as pd


class GetReceiptText:

    def getText(self):
        df = pd.read_csv('dataset.csv')
        receipt_no = df['Receipt_no']
        item_text = df['Item_Text']
        summary_text = df['Summary_Text']

        return receipt_no, item_text, summary_text

