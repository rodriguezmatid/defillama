import requests
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker


defi_url = "https://api.llama.fi/defi"
response = requests.get(defi_url)
data = response.json()

uniswap_tvl = data['currentChainTvls'] # Current TVL per chain
df = pd.DataFrame(uniswap_tvl)
df = df[['name', 'tvlUSD']]
df = df.rename(columns={'name': 'Protocol', 'tvlUSD': 'TVL'})

df['TVL'] = df['TVL'] / 1000000 # Convertir a millones de dólares
df['TVL'] = df['TVL'].round(2) # Redondear a dos decimales
df = df.sort_values(by="TVL", ascending=False)
print(df)

sns.set_style('whitegrid')
fig, ax = plt.subplots(figsize=(10, 6))

sns.barplot(x='Protocol', y='TVL', data=df, palette='Set2', alpha=0.8)
ax.set_xlabel('Protocol', fontsize=14, fontweight='bold')
ax.set_ylabel('TVL (Millions USD)', fontsize=14, fontweight='bold')
ax.set_title('TVL per DeFi Protocol', fontsize=18, fontweight='bold')

plt.xticks(fontsize=12, rotation=45)
plt.yticks(fontsize=12)

# Personalizar formato de los números en el eje Y
formatter = ticker.FuncFormatter(lambda x, p: '{:,.0f}M'.format(x))
ax.yaxis.set_major_formatter(formatter)

# Mostrar el valor encima de cada columna
for i, v in enumerate(df['TVL']):
    ax.text(i, v + 1000000, '${:,.2f}M'.format(v), ha='center', fontsize=10, fontweight='bold')

sns.despine(left=True, bottom=True)
plt.tight_layout()

plt.show()
