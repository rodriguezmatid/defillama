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

fig, ax1 = plt.subplots(figsize=(15, 10))
ax2 = ax1.twinx()

for i, chain in enumerate(chains):
    data_per_chain = data['chainTvls'][chain]['tvl']
    df_per_chain = pd.DataFrame(data_per_chain)
    df_per_chain['date'] = pd.to_datetime(df_per_chain['date'], unit='s')
    df_per_chain['totalLiquidityUSD'] = df_per_chain['totalLiquidityUSD'].div(1000000)  # convert to millions
    df_per_chain = df_per_chain[df_per_chain['date'] >= date_filter]
    if chain == 'Ethereum':
        ax2.plot(df_per_chain['date'], df_per_chain['totalLiquidityUSD'], label=chain, linewidth=2, color=colors[i])
        ax2.set_ylabel('Total Liquidity (Millions USD) - Ethereum', fontsize=14)  # update y-axis label
        ax2.yaxis.set_major_formatter(mtick.ScalarFormatter())  # update y-axis formatter
        ax2.ticklabel_format(style='plain', axis='y')  # disable scientific notation in y-axis
    else:
        ax1.plot(df_per_chain['date'], df_per_chain['totalLiquidityUSD'], label=chain, linewidth=2, color=colors[i])
        ax1.set_title('Total Liquidity on Different Chains', fontsize=16)
        ax1.set_xlabel('Date', fontsize=14)
        ax1.set_ylabel('Total Liquidity (Millions USD)', fontsize=14)  # update y-axis label
        # ax1.ticklabel_format(style='plain', axis='y')  # disable scientific notation in y-axis
        ax1.legend()
        ax1.yaxis.set_major_formatter(mtick.FuncFormatter(lambda x, p: format(int(x), ',')))
        # add a formatter to separate the thousands with a point (.) in the y-axis labels

plt.tight_layout()
plt.show()


