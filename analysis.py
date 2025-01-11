# %%

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

sns.set_theme(style="whitegrid")

# %%
df = pd.read_csv("results.txt", sep=";", header=None, names=["modo", "Tempo"])

df["Tipo Arquivo"] = df["modo"].apply(lambda x: x.split("_")[-1])
df["Tipo Engine"] = df["modo"].apply(lambda x: "-".join(x.split("_")[:-1]))


# Remover min e max
df_group = df.groupby(["modo"]).agg({"Tempo": ["min", "max"]}).reset_index()
df_group.columns = ["modo", "min", "max"]
df_group["tag"] = 1

df = (
    df.merge(df_group, left_on=["modo", "Tempo"], right_on=["modo", "min"], suffixes=[None, "_min"] ,how="left")
      .merge(df_group, left_on=["modo", "Tempo"], right_on=["modo", "max"], suffixes=[None, "_max"] ,how="left")
)

df = df[(df["tag"].isnull()) & (df["tag_max"].isnull())]

columns = ["modo","Tempo","Tipo Arquivo","Tipo Engine"]
df = df[columns]

# Sumário
df_summary = (df.groupby(["Tipo Arquivo","Tipo Engine"]).agg({"Tempo": ["mean", "std", "median"]})
              .reset_index())
df_summary.columns = ["Tipo Arquivo","Tipo Engine","Média","Desvio Padrão","Mediana"]
df_summary["Rate"] = df_summary["Média"] / df_summary["Média"].min()
df_summary = df_summary.round(4).sort_values(by=["Rate"])
print(df_summary.to_markdown(index=False))

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
