# %%

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

sns.set_theme(style="whitegrid")

# %%
df = pd.read_csv("results.txt", sep=";", header=None, names=["Tipo Engine", "Tipo Arquivo", "Tamanho", "Tempo"])

print(df.shape)
df.head()
# %%
# Remover min e max
col_groups = ["Tipo Engine", "Tipo Arquivo", "Tamanho"]
df_group = df.groupby(col_groups).agg({"Tempo": ["min", "max"]}).reset_index()
df_group.columns = col_groups + ["Min", "Max"]
df_group["tag"] = 1
df_group

# %%
df_join = (
    df.merge(df_group, left_on=col_groups+["Tempo"], right_on=col_groups+["Min"], suffixes=[None, "_min"] ,how="left")
      .merge(df_group, left_on=col_groups+["Tempo"], right_on=col_groups+["Max"], suffixes=[None, "_max"] ,how="left")
)

df_join
# %%
df_join = df_join[(df_join["tag"].isnull()) & (df_join["tag_max"].isnull())]
df_join = df_join[col_groups+["Tempo"]]
df_join

# %%
# Sumário
df_summary = (df_join.groupby(col_groups)
                     .agg({"Tempo": ["mean", "std", "median"]})
                     .reset_index())

df_summary.columns = col_groups + ["Média","Desvio Padrão","Mediana"]
df_summary["Rate"] = df_summary["Média"] / df_summary["Média"].min()
df_summary = df_summary.round(4).sort_values(by=["Rate"])
df_summary["Tamanho"] = df_summary["Tamanho"] / 1_000_000
print(df_summary.to_markdown(index=False))

# %%

palette = {
    'cudf_pandas': "#91c733",
    'pandas': "#f92727"
}

fig = plt.figure(figsize=(7, 6), dpi=900)
lnplot = sns.lineplot(
    data=df_summary,
    x="Tamanho",
    y="Média",
    hue="Tipo Engine",
    marker="o",
    palette=palette,
    alpha=0.7,   
)

lnplot.set(title="Curva de tempo execução por engine",
            xlabel="Quantidade de linhas (em milhões)",
            ylabel="Tempo médio (em segundos)")

fig.savefig("lineplot.png")
# %%

fig = plt.figure(figsize=(12, 6), dpi=900)

palette = {
    'cudf-pandas': "#91c733",
    'pandas': "#f92727"
}

barplot = sns.catplot(
    data=df_summary,
    kind='bar',
    x="Tipo Arquivo",
    y="Média",
    hue="Tipo Engine",
    palette=palette,
    alpha=0.7,   
)

barplot.set(title="Tempo de execução engine x arquivo",
            xlabel="Tipo Arquivo",
            ylabel="Média")


barplot.legend.set_title("")
plt.savefig("barplot.png")
