import requests
from bs4 import BeautifulSoup

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import streamlit as st
from bokeh.plotting import figure


url = 'https://www.imdb.com/chart/top/'
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

# Find the table that contains the movie data
table = soup.find('tbody', {'class': 'lister-list'})

# Create empty lists to store the movie data
titles = []
years = []
ratings = []
links = []

# Loop through each row in the table
for row in table.find_all('tr'):
    # Find the title, year, rating, and link for each movie
    title = row.find('td', {'class': 'titleColumn'}).find('a').text
    year = row.find('span', {'class': 'secondaryInfo'}).text.strip('()')
    rating = row.find('td', {'class': 'ratingColumn imdbRating'}).find('strong').text
    link = row.find('td', {'class': 'titleColumn'}).find('a')['href']
    
    # Append the movie data to the corresponding lists
    titles.append(title)
    years.append(year)
    ratings.append(rating)
    links.append(link)

# Create a dictionary with the movie data
movies_dict = {
    'Title': titles,
    'Year': years,
    'Rating': ratings,
    'Link': links
}

# Convert the dictionary to a Pandas DataFrame
movies_df = pd.DataFrame(movies_dict)
movies_df.to_csv('Movie.csv')

st.title("WEB SCRAPPING FOR IMDB DATA")


# Print the DataFrame
if st.button("All_Details"):
    st.write(movies_df)


if st.button("Top_10_ Movies"):
    #top 10
    top10 = movies_df.head(10)
    st.write("Top_10_Movies",top10)

if st.button("Above_9_Ratings "):
    
    #rating above 9
    top9rate = movies_df.drop (movies_df[ movies_df['Rating'] < "9"].index)
    st.write("RATING",top9rate)




st.title("Analysis with graphs")


if st.button("Line_graph"):    
    df = pd.read_csv('Movie.csv')
    # plot
    st.line_chart(data = df, x= "Year", y = "Rating")



    # Create a scatter plot
if st.button("Scatter_plot"):
    df = pd.read_csv('Movie.csv')
    fig, ax = plt.subplots()
    ax.scatter(df['Year'], df['Rating'])
    # Set plot title and axis labels
    ax.set_title('My Scatter Plot')
    ax.set_xlabel('Year')
    ax.set_ylabel('Rating')
    # Display plot in Streamlit
    st.pyplot(fig)

if st.button("bokeh plotting"):
    df = pd.read_csv('Movie.csv')
    

    # x = [1, 2, 3, 4, 5]
    # y = [6, 7, 2, 4, 5]

    p = figure(
    title='bokeh plotting',
    x_axis_label='Ratings',
    y_axis_label='Year')

    p.line( df['Rating'],df['Year'], legend_label='Trend', line_width=2)

    st.bokeh_chart(p, use_container_width=True)





