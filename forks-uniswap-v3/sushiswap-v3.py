import pandas as pd
import requests
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
import seaborn as sns
from datetime import datetime, timedelta

date_filter = '2023-04-01'
current_date = pd.Timestamp.now().strftime('%Y-%m-%d')

llama_url = "https://api.llama.fi/protocol/sushiswap-v3"
response = requests.get(llama_url)
data = response.json()

chain_list = ['Arbitrum', 'Optimism', 'Arbitrum Nova', 'Ethereum', 'Polygon', 'Avalanche', 'Binance', 'xDai', 'Fantom', 'Polygon zkEVM', 'Fuse', 'Moonriver', 'Moonbeam']
colors = ['blue', 'green', 'red', 'purple', 'orange', 'black']
df_dict = {}

for chain in chain_list:
    data_per_chain = data['chainTvls'][chain]['tvl']
    df_dict[chain] = pd.DataFrame(data_per_chain)
    df_dict[chain]['date'] = pd.to_datetime(df_dict[chain]['date'], unit='s')
    df_dict[chain]['date'] = df_dict[chain]['date'].dt.strftime('%Y-%m-%d')
    df_dict[chain]['chain'] = chain
    df_dict[chain] = df_dict[chain][(df_dict[chain]['date'] >= date_filter) & (df_dict[chain]['date'] < current_date)]
    df_dict[chain]['totalLiquidityUSD'] = df_dict[chain]['totalLiquidityUSD'].apply(lambda x: '{:,.0f}'.format(x))
    df_chain = df_dict[chain]
    print(df_chain)
    # df_for_table = df_dict.copy()

df_all_chains = pd.concat(df_dict.values(), ignore_index=True, axis=0)
df_all_chains['totalLiquidityUSD'] = pd.to_numeric(df_all_chains['totalLiquidityUSD'].str.replace(',', ''))
df_all_chains = df_all_chains.groupby('date')['totalLiquidityUSD'].sum().reset_index()
df_for_graphics = df_all_chains.copy()
df_all_chains['totalLiquidityUSD'] = df_all_chains['totalLiquidityUSD'].apply(lambda x: '{:,.0f}'.format(x))
print(df_all_chains)

sns.set_style('darkgrid')
plt.figure(figsize=(12,8))

sns.lineplot(data=df_for_graphics, x='date', y='totalLiquidityUSD', linewidth=2.5, color='firebrick')
plt.fill_between(data=df_for_graphics, x='date', y1='totalLiquidityUSD', alpha=0.2, color='red')

plt.title('Total Liquidity Across All Chains', fontsize=18, fontweight='bold', pad=20)
plt.xlabel('Date', fontsize=14, fontweight='bold', labelpad=15)
plt.ylabel('Total Liquidity (USD)', fontsize=14, fontweight='bold', labelpad=15)
plt.xticks(rotation=90, fontsize=12, fontweight='bold')
plt.yticks(fontsize=12, fontweight='bold')
plt.gca().yaxis.set_major_formatter(mtick.FuncFormatter(lambda x, _: '${:,.0f}'.format(x)))
plt.gca().spines['top'].set_visible(False)
plt.gca().spines['right'].set_visible(False)
plt.gca().spines['bottom'].set_linewidth(0.5)
plt.gca().spines['left'].set_linewidth(0.5)
plt.gca().tick_params(axis='x', length=8, width=0.5)
plt.gca().tick_params(axis='y', length=8, width=0.5)
plt.grid(True, alpha=0.5)
# plt.ylim(ymin=2500000000)

plt.tight_layout()
plt.show()