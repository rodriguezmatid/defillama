import requests
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick

llama_url = "https://api.llama.fi/protocol/uniswap"
response = requests.get(llama_url)
data = response.json()

chains = ['Optimism', 'Polygon', 'Celo', 'Arbitrum', 'Ethereum', 'BSC']
colors = ['blue', 'green', 'red', 'purple', 'orange', 'black']
date_filter = '2022-07-01'

fig, axs = plt.subplots(nrows=2, ncols=3, figsize=(15, 10))

for i, chain in enumerate(chains):
    data_per_chain = data['chainTvls'][chain]['tvl']
    df_per_chain = pd.DataFrame(data_per_chain)
    df_per_chain['date'] = pd.to_datetime(df_per_chain['date'], unit='s')
    df_per_chain['totalLiquidityUSD'] = df_per_chain['totalLiquidityUSD'].div(1000000)  # convert to millions
    df_per_chain = df_per_chain[df_per_chain['date'] >= date_filter]
    axs[i//3, i%3].plot(df_per_chain['date'], df_per_chain['totalLiquidityUSD'], label=chain, linewidth=2, color=colors[i])
    axs[i//3, i%3].set_title(f'Total Liquidity on {chain}', fontsize=16)
    axs[i//3, i%3].set_xlabel('Date', fontsize=14)
    axs[i//3, i%3].set_ylabel('Total Liquidity (Millions USD)', fontsize=14)  # update y-axis label
    axs[i//3, i%3].ticklabel_format(style='plain', axis='y')  # disable scientific notation in y-axis
    axs[i//3, i%3].legend()
    axs[i//3, i%3].set_xticklabels(axs[i//3, i%3].get_xticklabels(), rotation=45)  # rotate x-axis labels by 45 degrees
    axs[i//3, i%3].yaxis.set_major_formatter(mtick.FuncFormatter(lambda x, p: format(int(x), ',')))
    # add a formatter to separate the thousands with a point (.) in the y-axis labels

plt.tight_layout()
plt.show()