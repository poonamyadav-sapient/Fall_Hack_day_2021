import os
import json
import pandas as pd


class ReceiptValidation:
    def __init__(self):
        self.receiptData = {}
        self.getItem()
        self.getSummary()
        count=self.validateBasket()
        self.setReceiptInfo(count)

    def getItem(self):
        df = pd.read_csv('items.csv')
        for i in range(len(df['Receipt'])):
            items = {
                'rsd': df['Item_RSD'][i],
                'qty': int(df['Item_Qty'][i]),
                'amount': float(df['Item_Price'][i])
            }
            if str(df['Receipt'][i]) not in self.receiptData:
                self.receiptData[str(df['Receipt'][i])] = {'items': [items]}
            else:
                self.receiptData[str(df['Receipt'][i])]['items'].append(items)

    def getSummary(self):
        df = pd.read_csv('summary.csv')
        for i in range(len(df['Receipt'])):
            self.receiptData[str(df['Receipt'][i])]['subtotal'] = float(df['Subtotal'][i])
            self.receiptData[str(df['Receipt'][i])]['tax'] = float(df['Tax'][i])
            self.receiptData[str(df['Receipt'][i])]['total'] = float(df['Total'][i])

    def validateBasket(self):
        count = 0
        for receipts in self.receiptData:
            receipt = self.receiptData[receipts]
            items = receipt['items']
            basket_sum = format(sum(float(item['amount']) for item in items), ".2f")
            if (
                    basket_sum == format(receipt['subtotal'], ".2f") or
                    basket_sum == format(receipt['total'], ".2f") or
                    basket_sum == format(receipt['subtotal'], ".2f") + format(receipt['total'], ".2f") or
                    basket_sum == format(receipt['total'], ".2f") - format(receipt['tax'], ".2f")
            ):
                receipt['state'] = 'COMPLETE'
                count = count+1
            elif receipt['subtotal'] or receipt['total']:
                receipt['state'] = 'SUMMARY_PROCESS'
            else:
                receipt['state'] = 'ERROR_PARSING'

            self.receiptData[receipts] = receipt
        return count


    def setReceiptInfo(self,count):
        path = 'receipt_json/'
        try:
            os.mkdir(path)
        except:
            pass
        count1=0
        for receipts in self.receiptData:
            count1 = count1+1
            receipt = self.receiptData[receipts]
            print('{s} Ereceipt:{e} {s}'.format(s='*'*10, e=receipts))
            print('\nItem Data:')
            for items in receipt['items']:
                print('Item RSD: {}\nItem Qty: {}\nItem Price: {}\n'.format(items['rsd'], items['qty'], items['amount']))
            print('Summary Data:')
            print('Subtotal: {}\nTax: {}\nTotal: {}\n'.format(receipt['subtotal'], receipt['tax'], receipt['total']))
            print('State: {}\n'.format(receipt['state']))
            with open(path + receipts + ".json", "w") as file:
                json.dump(receipt, file, indent=3)
                file.close()
        print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\tTotal Complete state ereceipt:{0}/{1}\t~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~".format(count, count1))
