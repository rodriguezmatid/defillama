import requests
import dotenv as _dotenv
import os as _os
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

_dotenv.load_dotenv()

llama_url = "https://api.llama.fi/protocol/uniswap"
response = requests.get(llama_url)
data = response.json()

uniswap_tvl = data['currentChainTvls'] # Current TVL per chain
df = pd.DataFrame(list(uniswap_tvl.items()), columns=['Chain', 'TVL'])
df['TVL'] = df['TVL'].round(0)
df = df.sort_values(by="TVL", ascending=False)
df['Percentage'] = df['TVL'] / df['TVL'].sum()

df_for_table = df.copy()
total_tvl = df_for_table['TVL'].sum()
df_for_table['TVL'] = df_for_table['TVL'].apply(lambda x: '{:,.0f}'.format(x))
df_for_table['Percentage'] = df_for_table['Percentage'].apply(lambda x: '{:.2%}'.format(x))
print(df_for_table)

print("Total TVL: ", '{:,.0f}'.format(total_tvl))

# Formatear la columna "TVL" de la tabla con comas como separador de miles
sns.set_style('whitegrid')
fig, ax = plt.subplots(figsize=(10, 6))

sns.barplot(x='Chain', y='TVL', data=df, palette='Set2', alpha=0.8, ax=ax)
ax.set_xlabel('Chain', fontsize=14, fontweight='bold')
ax.set_ylabel('TVL (Millions USD)', fontsize=14, fontweight='bold')
ax.set_title('TVL per Chain', fontsize=18, fontweight='bold')

plt.xticks(fontsize=12, rotation=45)
plt.yticks(fontsize=12)

# Personalizar formato de los números en el eje Y
formatter = ticker.FuncFormatter(lambda x, p: '{:,.0f}M'.format(x / 1000000))
ax.yaxis.set_major_formatter(formatter)

# Mostrar el valor encima de cada columna
for i, v in enumerate(df['TVL']):
    ax.text(i, v + 100000000, '{:,.0f}M'.format(v / 1000000), ha='center', fontsize=10, fontweight='bold')

# Printear el monto total de TVL
total_tvl = df['TVL'].sum()
formatted_total_tvl = '{:,.0f}'.format(total_tvl)
plt.text(0.5, 1.1, f'Total TVL: {formatted_total_tvl} USD', horizontalalignment='center',
         verticalalignment='center', transform=ax.transAxes, fontsize=14)

sns.despine(left=True, bottom=True)
plt.tight_layout()
plt.show()
