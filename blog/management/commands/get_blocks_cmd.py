from django.core.management.base import BaseCommand, CommandError
import pandas as pd
import re
import requests
import json
from blog.models import latest_transactions,last_blocks


class Command(BaseCommand):

    def handle(self, *args, **options):
        def get_blocks():
            sats_conversion = 100000000
            last_blocks = requests.get('https://explorer.rise.vision/api/getLastBlocks')
            last_blocks_cleaned = json.loads(last_blocks.content)['blocks']
            df = pd.DataFrame(last_blocks_cleaned)
            lst = []
            for dct in df['delegate'].tolist():
                lst.append((dct['username'], dct['rank']))

            df['username'] = ''
            df['rank'] = ''

            for ix in range(len(df)):
                df['username'].ix[ix] = lst[ix][0]
                df['rank'].ix[ix] = lst[ix][1]

            df.head(5)
            del df['delegate']

            df_cols = [x for x in df.columns.tolist()]
            block_cols = ['generator', 'height', 'blockid', 'reward', 'timestamp', 'totalamount', 'totalfee',
                          'totalforged', 'transactionscount', 'username', 'rank']
            columns = {x: y for (x, y) in zip(df_cols, block_cols)}
            df.rename(columns=columns, inplace=True)

            df['reward'] = df['reward'] / sats_conversion
            df['totalamount'] = df['totalamount'] / sats_conversion
            df['totalfee'] = df['totalfee'] / sats_conversion
            df['totalforged'] = df['totalforged'] / sats_conversion

            return df

        df = get_blocks()
        X = df.itertuples()
        f = open('get_blocks_log', 'w')
        print(X)
        while True:
            try:
                Y = last_blocks()
                resp = zip(df.columns.tolist(), X.next()[1:])
                for ix in resp:

                    print(ix[0], ix[1])
                    if ix != 'id':
                        setattr(Y, str(ix[0]), ix[1])
                Y.save()
            except StopIteration:
                break

            except Exception as e:
                f.write(str(e))
                f.write('\n')
                f.write(str('resp'))
                f.write('\n')
        f.close()
