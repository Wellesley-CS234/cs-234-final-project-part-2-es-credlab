import streamlit as st
import pandas as pd
import math
import plotly.graph_objects as go
import plotly.express as px

st.set_page_config(layout="wide")

st.title("Feminist Popularity based on Wave of Feminism")
st.write('''The page is dedicated to analyze the popularity of each wave of feminism (first, second, and third wave, excluding the fourth wave)
         and the potential for a feminist's wave could infl;uence their popularity on Wikipedia.
         Wave popularity is determined by the average article pageviews per day that feminist articles who are
         associated with that specified wave recieve and the total pageviews those articles recieve over the seven day testing period.
         ''')
st.write("The first few visualizations break down basci summary statistics about each wave of feminism depending on the feminists who are associated " \
"with that wave. The last line plot is associated with the widget where you can select which waves of feminism to compare.")

# line plot comparing birth-year of feminist 
## ---prepare data for analysis---
line_plot_df = pd.read_csv("data/line_plot_average_pageviews.csv")[['Birthyear','average_pageviews']]

line_plot_df["Birthyear"] = pd.to_datetime(line_plot_df["Birthyear"], errors="coerce")

line_plot_df.sort_values(by="Birthyear",inplace=True)

min_date = line_plot_df["Birthyear"].min().date()
max_date = line_plot_df["Birthyear"].max().date()

## ---create widget---
start_date, end_date = st.date_input(
    "Select date range to get started - ",
    (min_date, max_date),
    min_value=min_date,
    max_value=max_date
)

filtered_df = line_plot_df[(line_plot_df["Birthyear"].dt.date >= start_date) & (line_plot_df["Birthyear"].dt.date <= end_date)]

## ---create plot---
fig = px.line(
    line_plot_df,
    x="Birthyear",
    y="average_pageviews",
    title="Pageviews of Feminist Article based on Feminist Birth-Year",
    markers=True
)

st.plotly_chart(fig, use_container_width=True)

# popularity of feminists based on wave (average pageviews)

## ---create data---
list_of_feminists = pd.read_csv("data/line_plot_average_pageviews.csv")
wave_present = list_of_feminists[list_of_feminists['wave'].notna()]

grouped_mean = wave_present.groupby('wave')['average_pageviews'].mean()
grouped_count = wave_present.groupby('wave')['Name'].count()
grouped_sum = wave_present.groupby('wave')['average_pageviews'].sum()

grouped_df = pd.DataFrame({'Wave':grouped_mean.index,'Count':grouped_count.values,'Average Pageviews':grouped_mean.values,'Total Pageviews Sum':grouped_sum.values})

## most viewed feminists
st.dataframe(grouped_df)

col1, col2 = st.columns([1, 1])
## ---create bargraph of average pageviews and total pageviews sum---
with col1:
    st.write("Feminist Pageviews by Wave")
    st.bar_chart(
    grouped_df,
    x='Wave',
    y=['Average Pageviews','Total Pageviews Sum'],
    x_label='Number of Pageviews',
    horizontal=True # Set to True for a horizontal orientation
    )

## ---create bargraph of wave count---
with col2:
    st.write("Number of Feminist Articles by Wave")
    st.bar_chart(
    grouped_df,
    x='Wave',
    y='Count',
    x_label='Number of Related Articles',
    horizontal=False # Set to True for a horizontal orientation
    )

st.write('''From the above visualizations, we can see that second-wave feminism has the highest average pageviews and total pageviews sum, 
         as well as the highest number of feminists. First-wave feminism has the lowest average pageviews and total pageviews sum, as
         well as the fewest number of feminists and their related articles. The above linegraph further supports this observation,
         as the highest viewed feminists were born around 1950, which would align with them contributing to the second wave of feminism.''')

selected_wave = st.multiselect('Select a wave to get started - ', ['First-wave','Second-wave','Third_wave'])
# average pageviews based on wave of feminism over the 7-day period

## ---create data---
pageview_data = pd.read_csv("data/cleaned_pageview_data.csv")
pageview_data = pageview_data[pageview_data['wave'].notna()]

grouped_2 = pageview_data.groupby(['date_object','wave'])['pageviews'].mean()

grouped_2_df = pd.DataFrame({'Day':[0,0,0,1,1,1,2,2,2,3,3,3,4,4,4,5,5,5,6,6,6],'Wave':['First-wave','Second-wave','Third_wave']*7,"Mean Pageviews":grouped_2.values})

## create widget
grouped_2_df = grouped_2_df[grouped_2_df['Wave'].isin(selected_wave)]

## ---create line-plot---
fig = px.line(
    grouped_2_df,
    x="Day",
    y="Mean Pageviews",
    color='Wave',
    title="Mean Pageviews of Articles based on Wave of Feminism Over 7 Day Period",
    markers=True
    )

st.plotly_chart(fig, use_container_width=True)

st.dataframe(grouped_2_df)

st.write('''The line plot above contradicts some previous findings, as the line plot shows that first-wave feminists are the most viewed on
         average over the seven day testing period, whereas second-wave feminists had the highest total pageviews in the previous bar chart.
         Therefore, the wave that a feminist is associated with may impact their popularity on Wikipedia, especially if they are a member of the second wave
         of feminism.''')