import pandas as pd
import requests
from tqdm import tqdm
import time

time.sleep(5)
df = pd.read_csv('./augmented.csv')
while True:
    for row in tqdm(df.to_dict(orient='records'), total=len(df)):
        resp  = requests.post('http://server:8000/data', json=row, headers={'Content-Type': 'application/json'})
        time.sleep(.01)
