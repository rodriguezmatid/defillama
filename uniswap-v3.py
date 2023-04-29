import requests
import dotenv as _dotenv
import os as _os
import pandas as pd
from datetime import datetime
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker



_dotenv.load_dotenv()

llama_url = "https://api.llama.fi/protocol/uniswap"
response = requests.get(llama_url)
data = response.json()

dataPerChain = data['chainTvls']['Ethereum']['tvl']
df = pd.DataFrame(dataPerChain)

# convertir la columna 'date' en una fecha y quedarnos solo con el día
df['date'] = pd.to_datetime(df['date'], unit='s').dt.strftime('%d-%m-%Y')
# redondear la columna 'totalLiquidityUSD' a números enteros
df['totalLiquidityUSD'] = df['totalLiquidityUSD'].round(0)

# agregar separador de miles en la columna 'totalLiquidityUSD'
df['totalLiquidityUSD'] = df['totalLiquidityUSD'].apply(lambda x: '{:,.0f}'.format(x).replace(',', '.'))
print(df)

uniswap_tvl = data['currentChainTvls'] # Current TVL per chain
df = pd.DataFrame(list(uniswap_tvl.items()), columns=['Chain', 'TVL'])
df = df.sort_values(by="TVL", ascending=False)
print(df)
# df["TVL"] = df["TVL"].apply(lambda x: x / 1000000)

fig, ax = plt.subplots()

ax.bar(df['Chain'], df['TVL'] / 1000000, color='blue')

ax.set_xlabel('Chain')
ax.set_ylabel('TVL (en millones)')
ax.set_title('TVL por Chain')

plt.xticks(rotation=45)

# Personalizar formato de los números en el eje Y
formatter = ticker.FuncFormatter(lambda x, p: format(int(x), ','))

# Aplicar el formato al eje Y
ax.yaxis.set_major_formatter(formatter)

# Mostrar el valor encima de cada columna
for i, v in enumerate(df['TVL']):
    ax.text(i, v / 1000000 + 1, format(int(v), ','), ha='center', fontsize=8)

plt.show()
# uniswap_tvl = data['chainTvls']['Ethereum'] # Historical TVL in Ethereum
# uniswap_tvl = data['chainTvls']['Optimism'] # Historical TVL in Optimism
# uniswap_tvl = data['chainTvls']['BSC'] # Historical TVL in BSC
# uniswap_tvl = data['chainTvls']['Polygon'] # Historical TVL in Polygon
# uniswap_tvl = data['chainTvls']['Celo'] # Historical TVL in Celo
# uniswap_tvl = data['chainTvls']['Arbitrum'] # Historical TVL in Arbitrum

# variable = requests.get(API_BASE_URL).json()['tokens'][-1]['date']
# variable = datetime.fromtimestamp(1643414400)
# print(variable)

# ts = requests.get(API_BASE_URL)
# ts = ts.json()
# ts = ts['tokens'][-1]
# df = pd.DataFrame(ts)
# df = df.drop(columns=['date']).round().astype(int)
# print(df)