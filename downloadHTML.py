from boto3.session import Session

from dotenv import load_dotenv
import os

load_dotenv(dotenv_path='creds.env')



import snowflake.connector
import os
from dotenv import load_dotenv
import argparse
import json
import boto3


class GetFileNames:
    def __init__(self):
        parser = argparse.ArgumentParser()
        args = self.getArgs(parser)
        self.fetchReceipts(args)

    def getArgs(self, parser):
        parser.add_argument('-banner_key', '--banner_key', help='Enter banner key')
        parser.add_argument('-start_date', '--start_date', help='Enter start date of the receipts')
        parser.add_argument('-limit', '--limit', default=10, help='Enter number of receipts required')

        args = parser.parse_args()
        return args

    def snowflake_connector(self):

        username = os.getenv('username')
        password = os.getenv('password')

        ctx = snowflake.connector.connect(
            user=username,
            password=password,
            account='infoscout',
            database='infoscout',
            authenticator='externalbrowser'
        )

        cs = ctx.cursor()
        return cs

    def fetchReceipts(self, args):
        cs = self.snowflake_connector()

        cs.execute("USE warehouse ISC_DW")

        receipts = cs.execute(
        '''
        select ID, HTML_EMAIL
        from INFOSCOUT.PRICESCOUT.RDL_ERECEIPT
        where BANNER_KEY = '{}'
        and TRANSACTION_DATETIME > '{}'
        and STATE = 'COMPLETE'
        LIMIT {}
        '''.format(args.banner_key, args.start_date, args.limit)).fetchall()

        cs.close()

        receipt_data = []
        for receipt in receipts:
            receipt_data.append({"ID": receipt[0], "receipt": receipt[1]})

        with open("file_names.json", "w") as file:
            json.dump(receipt_data, file, indent=3)
            file.close()

        self.downloadHtml(receipt_data)

    def downloadHtml(self, receipt_data):
        ACCESS_KEY_ID = os.getenv('ACCESS_KEY_ID')
        SECRET_ACCESS_KEY = os.getenv('SECRET_ACCESS_KEY')
        path = 'html_files/'
        s3 = boto3.client('s3', aws_access_key_id=ACCESS_KEY_ID, aws_secret_access_key=SECRET_ACCESS_KEY)

        for receipts in receipt_data:
            s3.download_file('isc.pricescout.ecomm', receipts['receipt'], path + str(receipts['ID']))
            print("\nDownloaded receipt:", receipts['ID'])

if __name__ == "__main__":
    GetFileNames()

