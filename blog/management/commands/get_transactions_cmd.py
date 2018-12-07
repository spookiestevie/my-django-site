from django.core.management.base import BaseCommand, CommandError
import requests
import json
import pandas as pd
import re
from blog.models import latest_transactions,last_blocks

class Command(BaseCommand):
	
	def handle(self, *args, **options):
		def get_transactions():
			sats_conversion = 100000000
			last_transactions = requests.get('https://explorer.rise.vision/api/getLastTransactions')
			last_transactions_cleaned = json.loads(last_transactions.content)['transactions']
			zf = pd.DataFrame(last_transactions_cleaned)

			to_del = ['asset', 'blockId', 'knownRecipient', 'knownSender', 'recipientDelegate', 'recipientPublicKey',
					  'requesterPublicKey', 'rowId', 'senderDelegate', 'senderPublicKey', 'signSignature', 'signature',
					  'signatures', ]
			desired_cols = [x for x in zf.columns.tolist() if x not in to_del]

			zf = zf[desired_cols]

			zf = zf.rename(columns={x[0]: x[1].lower() for x in zip(zf.columns.tolist(), zf.columns.tolist())})

			zf = zf[['id', 'amount', 'fee', 'height', 'senderid', 'timestamp', 'recipientid', 'type', 'confirmations']]

			sort_me = """
		    txid = models.BigIntegerField()
		    amount = models.BigIntegerField()
		    fee = models.BigIntegerField()
		    height = models.BigIntegerField()
		    senderid = models.CharField(max_length=50)
		    timestamp = models.BigIntegerField()
		    recipientid = models.CharField(max_length=50)
		    txtype = models.BigIntegerField()
		    confirmations = models.BigIntegerField()
		    """

			lst = sort_me.split('\n')
			tx_cols = []
			for ix in lst:
				if ix:
					resp = re.split(' =', ix)
					tx_cols.append(resp[0].strip())
			curr_tx_cols = zf.columns.tolist()
			columns = {x: y for (x, y) in zip(curr_tx_cols, tx_cols)}
			zf.rename(columns=columns, inplace=True)

			zf['amount'] = zf['amount'] / sats_conversion
			zf['fee'] = zf['fee'] / sats_conversion

			return zf

		zf = get_transactions()
		X = zf.itertuples()
		f = open('get_transactions_log','w')
		print(X)
		while True:
		    try:
			Y = latest_transactions()
			resp = zip(zf.columns.tolist(),X.next()[1:])
		    
			for ix in resp:
		    
				print ix[0],ix[1]
				if ix != 'id':
				    setattr(Y,str(ix[0]),ix[1])
			Y.save()
		    except StopIteration:
			break 
			
		    except Exception as e:
			f.write(str(e))
			f.write('\n')
			f.write(str('resp'))
			f.write('\n')
		f.close()
			
