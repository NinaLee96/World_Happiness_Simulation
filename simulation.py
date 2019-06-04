import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from tkinter import *
from tkinter import ttk
import matplotlib.pyplot as plt
import seaborn as sns
from mpldatacursor import datacursor     #pip install mpldatacursor
from pathlib import Path

sns.set()

plt.matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure


# Read CSV File
data_folder = Path("World_Happiness/World_Happiness/data")
filename1 = data_folder / "happiness_cleaned.csv"
filename2 = data_folder / "economy_cleaned.csv"
filename3 = data_folder / "freedom_cleaned.csv"
filename4 = data_folder / "health_cleaned.csv"

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


def reset_dataframes():
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

def calculate_happiness():
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
    happiness_df = mergedStuff[['Country','Happiness Score','Economy (GDP per Capita)','Health (Life Expectancy)','Freedom']]
    # added Country list to the merge ^

def calculate_economy_score():
    global economy_df
    economy_df['2019 Score'] = economy_df.iloc[:, -(len(economy_df.columns)):].sum(axis=1)
    economy_df['2019 Score'] = economy_df['2019 Score']/(len(economy_df.columns)-1)

def calculate_freedom_score():
    global freedom_df
    freedom_df['hf_score'] = freedom_df.iloc[:, -(len(freedom_df.columns)-1):].sum(axis=1)
    freedom_df['hf_score'] = freedom_df['hf_score']/(len(freedom_df.columns)-2)

def insert_new_value(country, dataset, column, value):
    global happiness_df
    global economy_df
    global freedom_df
    global health_df
    reset_dataframes()
    # print(country, dataset, column, value )
    if (dataset == 'Economy'):
        economy_df.loc[economy_df['Country'] == country, column] = value
        calculate_economy_score()
        calculate_happiness()
    elif (dataset == 'Freedom'):
        freedom_df.loc[freedom_df['Country'] == country, column] = value
        calculate_freedom_score()
        calculate_happiness()
    elif (dataset == 'Health'):
        health_df.loc[health_df['Country'] == country, column] = value
        calculate_happiness()
    else:
        print('Something went wrong...')

# Event handler for Dots on the Graph
def myformatter(**kwarg):
    label = '{x:.0f}'.format(**kwarg)
    print('label is ', label, type(label))
    # print(happiness_df['Country'])
    print(happiness_df.loc[int(label)])
    dot_handler = happiness_df.loc[int(label)]
    selected_country = dot_handler['Country']
    happy = dot_handler['Happiness Score']
    return selected_country, int(happy)

# Event handler for quit button
def quit():
    root.quit()

# Getter function for okay button
def ok():
    print("Country selected", country_list.get())
    print("Dataset selected:", dataset_list.get())
    print("Column selected:", column_list.get())
    print("Entered value:", text_field.get())

    global country
    global dataset
    global dataset_columns
    global value 
    global happiness_df
    
    country = country_list.get()
    dataset = dataset_list.get()
    dataset_columns = column_list.get()
    value = text_field.get()
    # print(type(int(value)))
    # print(happiness_df.head())
    print()
    print('Before')
    print()
    print(happiness_df.describe())

    insert_new_value(country, dataset, dataset_columns, float(value))
    print()
    print('After')
    print()
    print(happiness_df.describe())

    df1 = pd.read_csv(filename1, encoding='latin-1', sep='\t')
    # print
    # print(df1.head())
    # print(happiness_df.head())
    print(len(list(happiness_df['Country'])))
    print(len(list(happiness_df['Happiness Score'])))

    #================== matplot Graph ====================#

    # dimensions = (18, 12)
    # fig, ax = plt.subplots(figsize=dimensions)
    # sns.scatterplot(x="Country", y="Happiness Score", data=happiness_df, ax=ax)
    # plt.xticks(fontsize=8,rotation=90)
    # ax.set(ylabel='Country', xlabel='Happiness Score', title='World Happiness by Country')

    figure1 = plt.Figure(figsize=(14,5.7), dpi=100)
    ax1 = figure1.add_subplot(111)
    ax1.scatter(list(happiness_df['Country']), list(happiness_df['Happiness Score']), color='g')
    print(happiness_df.loc[happiness_df['Country'] == country])
    query_df = happiness_df.loc[happiness_df['Country'] == country]

    ax1.scatter(query_df['Country'], query_df['Happiness Score'], color='r')
    # ax1.scatter(happiness_df[country], happiness_df[country], color='r')
    scatter1 = FigureCanvasTkAgg(figure1, root)
    plt.xticks(fontsize=6,rotation=90)
    ax1.set_xticklabels(list(happiness_df['Country']), rotation=90, fontsize=9)
    
    datacursor(ax1, formatter=myformatter)
    scatter1.get_tk_widget().grid(row=8,pady=10, padx=10)

    ax1.set_title(label='World Happiness by Country')
    ax1.set_xlabel('Country')
    ax1.set_ylabel('Happiness Score')

    #========================================================#

# Event handler, handles drop down menu change
def callback(event):
    global dataset_columns_array
    global column_list
    print("variable changed")
    
    if dataset_list.get() == "Economy":
        gui_economy_df = pd.read_csv(filename2, encoding='latin-1', sep='\t', nrows=0)
        # print()
        # print(list(economy_df)[3:])
        # print()
        dataset_columns_array = list(gui_economy_df)[3:]
        column_var.set(dataset_columns_array[0])
        column_list = ttk.Combobox(root, values=dataset_columns_array)
        column_list.current(0)
        column_list.configure(font=("Arial", 12))
        column_list.grid(row=5)

    elif dataset_list.get() == "Freedom":
        gui_freedom_df = pd.read_csv(filename3, encoding='latin-1', sep='\t', nrows=0)
        # print()
        # print(list(freedom_df)[2:])
        # print()
        dataset_columns_array = list(gui_freedom_df)[2:]
        column_var.set(dataset_columns_array[0])
        column_list = ttk.Combobox(root, values=dataset_columns_array)
        column_list.current(0)
        column_list.configure(font=("Arial", 12))
        column_list.grid(row=5)

    else:
        gui_health_df = pd.read_csv(filename4, encoding='latin-1', sep='\t', nrows=0)
        # print()
        # print(list(health_df)[:])
        # print()
        dataset_columns_array = list(gui_health_df)[2:]
        column_var.set(dataset_columns_array[0])
        column_list = ttk.Combobox(root, values=dataset_columns_array)
        column_list.current(0)
        column_list.configure(font=("Arial", 12))
        column_list.grid(row=5)


# Populates country list in GUI
countries_df = pd.read_csv(filename1, encoding='latin-1', sep='\t')
country_array = list(countries_df["Country"])
 
# Populates column list in GUI
gui_economy_df = pd.read_csv(filename2, encoding='latin-1', sep='\t', nrows=0)
dataset_columns_array = list(gui_economy_df)[3:]

# Initialize the screen
root = Tk()

# Set screen size
root.geometry("1600x800")
# Set screen title
root.title("Happiness GUI")


# Configures the grid for column 0
root.grid_columnconfigure(0, weight=1)

# Countries drop down menu
Label(root, text="Select a Country").grid(row=0)
var = StringVar()
var.set(country_array[0])
country_list = ttk.Combobox(root, values=country_array)
country_list.current(0)
country_list.configure(font=("Arial", 12))
country_list.grid(row=1)

# Dataset drop down menu
Label(root, text="Select a Dataset").grid(row=2)
dataset_array = ["Economy", "Freedom", "Health"]
dataset_var = StringVar()
dataset_var.set(dataset_array[0])
dataset_list = ttk.Combobox(root, values=dataset_array)
dataset_list.current(0)
dataset_list.configure(font=("Arial", 12))
dataset_list.grid(row=3)

# Triggers event handler 
dataset_list.bind("<<ComboboxSelected>>", callback)


# Columns of dataset drop down menu
Label(root, text="Select a Column from the Dataset").grid(row=4)
column_var = StringVar()
column_var.set(dataset_columns_array[0])
column_list = ttk.Combobox(root, values=dataset_columns_array)
column_list.current(0)
column_list.configure(font=("Arial", 12))
column_list.grid(row=5)

# Text Field for user input
Label(root, text="Insert a Numeric Value").grid(row=6)
text_field = Entry(root, width=33)
text_field.grid(row=7, ipady=3)

# Ok button that calls function
button = Button(root, text="OK", command=ok, width=25)
button.grid(row=8, pady=20, padx=10)
button = Button(root, text="Quit", command=quit, width=25)
button.grid(row=8, column=1, pady=20, padx=10)

# Initialize, creates a happiness baseline (REQUIRED)
calculate_happiness()

# Happiness before value insertion
print(happiness_df.describe())

# insert_new_value('Denmark', 'Economy', 'Property Rights', 9000)

#After value insertion
# print(happiness_df.describe())

root.mainloop()
