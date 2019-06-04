import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Read CSV File
filename1 = '/Users/bryceremick/Desktop/World_Happiness/data/happiness_cleaned.csv'
filename2 = '/Users/bryceremick/Desktop/World_Happiness/data/economy_cleaned.csv'
filename3 = '/Users/bryceremick/Desktop/World_Happiness/data/freedom_cleaned.csv'
filename4 = '/Users/bryceremick/Desktop/World_Happiness/data/health_cleaned.csv'

happiness_df = pd.read_csv(filename1, encoding='latin-1', sep='\t')
economy_df = pd.read_csv(filename2, encoding='latin-1', sep='\t')
freedom_df = pd.read_csv(filename3, encoding='latin-1', sep='\t')
health_df = pd.read_csv(filename4, encoding='latin-1', sep='\t')

happiness_df = happiness_df.drop(columns=['Unnamed: 0'])
economy_df = economy_df.drop(columns=['Unnamed: 0'])
freedom_df = freedom_df.drop(columns=['Unnamed: 0'])
health_df = health_df.drop(columns=['Unnamed: 0'])

freedom_df = freedom_df.rename(index=str, columns={"countries": "Country"})
health_df = health_df.rename(index=str, columns={"Country Name": "Country"})
freedom_df = freedom_df.drop_duplicates(subset='Country', keep='first')


def resetDataframes():
    global happiness_df
    global economy_df
    global freedom_df
    global health_df
    happiness_df = pd.read_csv(filename1, encoding='latin-1', sep='\t')
    economy_df = pd.read_csv(filename2, encoding='latin-1', sep='\t')
    freedom_df = pd.read_csv(filename3, encoding='latin-1', sep='\t')
    health_df = pd.read_csv(filename4, encoding='latin-1', sep='\t')
    happiness_df = happiness_df.drop(columns=['Unnamed: 0'])
    economy_df = economy_df.drop(columns=['Unnamed: 0'])
    freedom_df = freedom_df.drop(columns=['Unnamed: 0'])
    health_df = health_df.drop(columns=['Unnamed: 0'])
    freedom_df = freedom_df.rename(index=str, columns={"countries": "Country"})
    health_df = health_df.rename(index=str, columns={"Country Name": "Country"})
    freedom_df = freedom_df.drop_duplicates(subset='Country', keep='first')

def calculateHappiness():
    global happiness_df
    global economy_df
    global freedom_df
    global health_df
    mergedStuff = pd.merge(happiness_df, economy_df, on=['Country'], how='inner')
    mergedStuff = pd.merge(mergedStuff, freedom_df, on=['Country'], how='inner')
    mergedStuff = pd.merge(mergedStuff, health_df, on=['Country'], how='inner')
    mergedStuff['Freedom'] = mergedStuff['Freedom'] * mergedStuff['hf_score']
    mergedStuff['Health (Life Expectancy)'] = mergedStuff['Health (Life Expectancy)'] * mergedStuff['2016']
    mergedStuff['Economy (GDP per Capita)'] = mergedStuff['Economy (GDP per Capita)'] * mergedStuff['2019 Score']
    mergedStuff['Happiness Score'] = mergedStuff['Freedom'] + mergedStuff['Health (Life Expectancy)'] + mergedStuff['Economy (GDP per Capita)']
    happiness_df = mergedStuff[['Happiness Score','Economy (GDP per Capita)','Health (Life Expectancy)','Freedom']]


calculateHappiness()
print(happiness_df.mean())
resetDataframes()
economy_df.loc[economy_df['Country'] == 'United States', '2019 Score'] = 1000
calculateHappiness()
print(happiness_df.mean())