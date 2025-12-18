import pandas as pd
import streamlit as st
import plotly.express as px
from pathlib import Path

st.set_page_config(layout="wide")

st.title("Geographical Analysis of Feminist Popularity")
st.write('''This page is dedicated to a geographical analysis of the feminists listed in Wikipedia's 'List of Feminists' article.
         The three analysis aviable on this page are as follows - \n
         \t1. Number of Feminists from Each Country (According the the 'List of Feminists' Wikipedia Page)
         \t2. Total Pageviews for Feminists from Each Country over the Seven Day Data Collection Period.
         \t3. Average Pageviews Each Feminist Article Receives per Day for Each Country''')
st.write('''** The dataframe below also shows the top country depending on the selected category.''')

# ---prepare universal data---
ROOT = Path(__file__).resolve().parents[1]
CSV_PATH = ROOT / "data" / "list_of_feminists.csv"

list_of_feminists = pd.read_csv(CSV_PATH)

pageview_data = pd.read_csv("data/cleaned_pageview_data.csv")

# ---create universal widget---
selected_analysis = st.selectbox('Pick an analysis to get started - ', ['Number of Feminists','Total Article Pageviews','Average Article Pageviews'])

if selected_analysis == 'Number of Feminists':

    ## ---prepare data for analysis---
    grouped = list_of_feminists.groupby("Country")['q_id'].count()
    origin_information_df = grouped.reset_index()
    origin_information_df.columns = ["Country","Count"]

    st.write(type(origin_information_df['Count'][0]))

    ## ---prepare chloropleth for frequency visualization---
    fig = px.choropleth(origin_information_df, 
                        locations="Country", 
                        locationmode='country names', 
                        color="Count",
                        color_continuous_scale="pinkyl",
                        width=1000,
                        height=600)
    origin_information_df.sort_values("Count",ascending=False,inplace=True)
    dataframe = origin_information_df
else:
    ## ---prepare data for analysis---
    target_qids = list_of_feminists.q_id

    pageviews = [[pageview_data['qid'][index],pageview_data['pageviews'][index]] for index in pageview_data.index if pageview_data['qid'][index] in target_qids.values]
    grouped = pd.DataFrame(pageviews,columns=['q_id','pageviews']).groupby('q_id').mean()
    target_information_df = grouped.reset_index()
    target_information_df.columns = ['q_id','Total Article Pageviews']

    pageview_df = pd.merge(list_of_feminists[["Country","q_id"]], target_information_df, on='q_id', how='inner')
    pageview_df.sort_values('Total Article Pageviews',ascending=False,inplace=True)
    pageview_df['Rounded Total Article Pageviews'] = pageview_df['Total Article Pageviews'].apply(lambda x: round(x))
    
    ## ---prepare chloropleth for pageviews visualization---
    if selected_analysis == 'Total Article Pageviews':
        fig = px.choropleth(pageview_df, 
                        locations="Country", 
                        locationmode='country names', 
                        color="Rounded Total Article Pageviews",
                        color_continuous_scale="pinkyl",
                        width=1000,
                        height=600)
        pageview_df.sort_values("Rounded Total Article Pageviews",ascending=False,inplace=True)
        dataframe = pageview_df
    else:
        grouped_again = pageview_df.groupby("Country")['Total Article Pageviews'].mean()
        average_pageviews_df = grouped_again.reset_index()
        average_pageviews_df.columns = ['Country','Average Article Pageviews']
        average_pageviews_df['Rounded Average Article Pageviews'] = average_pageviews_df['Average Article Pageviews'].apply(lambda x: round(x))

        fig = px.choropleth(average_pageviews_df, 
                        locations="Country", 
                        locationmode='country names', 
                        color="Rounded Average Article Pageviews",
                        color_continuous_scale="pinkyl",
                        width=1000,
                        height=600)
        average_pageviews_df.sort_values("Rounded Average Article Pageviews",ascending=False,inplace=True)
        dataframe = average_pageviews_df

st.plotly_chart(fig)

st.write(f'''Top 10 Countries for '{selected_analysis}' ''')
st.dataframe(dataframe)

st.write('''We can see from the above analysis that the most amount of feminists listed on Wikipedia come from the United States,
         and many of the feminists are also from the West. This trend continiues with the Total Article pageviews,
         as the United States and the Western world have the most amount of feminist pageviews. Wikipedioa's representation
         of feminists is clearly skewed towards the Western World, which may indicate a lack of representation in Wikipedia editors. 
         Nevertheless, it is important to bring attention to this bias, as it may impact a feminist's popularity and visibility on the internet.''')