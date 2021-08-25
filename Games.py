import pandas as pd
import pandera as pa
import numpy as np
import matplotlib.pyplot as plt

#Carregamento dos dados do arquivo fonte .CSV carregado no Google drive.
valores_ausentes = ["N/A"]#Define os valores nulos
df = pd.read_csv("/content/drive/MyDrive/Datasets/vgsales.csv", sep=",", na_values=valores_ausentes)#leitura do .csv com auxilio da biblioteca pandas
df.head(10)

#Validando os dados com a biblioteca pandera.
schema = pa.DataFrameSchema(
    columns = {
        "Name":pa.Column(pa.String),
        "Platform":pa.Column(pa.Object),
        "Genre":pa.Column(pa.Object),
        "Publisher":pa.Column(pa.String, nullable=True),
        "NA_Sales":pa.Column(pa.Float),
        "EU_Sales":pa.Column(pa.Float),
        "JP_Sales":pa.Column(pa.Float),
        "Other_Sales":pa.Column(pa.Float),
        "Global_Sales":pa.Column(pa.Float)
    }
)

schema.validate(df)

#Renomeando nome das colunas.
df.rename(columns={"Name":"Nome", 
                   "Platform":"Plataforma", 
                   "Year":"Ano", 
                   "Genre":"Genero", 
                   "NA_Sales":"NA_Vendas", 
                   "EU_Sales":"JP_Vendas", 
                   "Other_Sales":"Outras_Vendas", 
                   "Global_Sales":"Vendas_Totais"}, inplace=True)

#Definindo a coluna "Rank" como indice.
df.set_index('Rank', inplace=True)

#passa todos os anos diferentes de nulo para a df2 e exibe os 10 mais recentes
filtro= df.Ano > 0 
df2 = df.loc[filtro]
df2.nlargest(10, "Ano")

#exibe um grafico de tabela que mostra o total de jogos registrados por plataforma.
plt.style.use("ggplot")
df["Plataforma"].value_counts().plot.bar(title="Total de jogos por plataforma",figsize=(15, 15), color="green")
plt.xlabel("Plataforma")
plt.ylabel("Total jogos")

#exibe um grafico de pizza que mostra o total de vendas registrados por genero.
plt.style.use("ggplot")
df.groupby(df["Genero"])["Vendas_Totais"].sum().plot.pie(title="Total de vendas por genero",figsize=(15, 15))
plt.ylabel("Total de vendas")
plt.legend()

#Cria um csv apenas com a Plataforma de PS2
filtro= df.Platforma.str.contains ('PS2') #possuem RIO
df2 = df.loc[filtro]
df2
df2 = df2.to_csv("/content/drive/MyDrive/Datasets/TESTE GAMES.csv")#salva em google drive
