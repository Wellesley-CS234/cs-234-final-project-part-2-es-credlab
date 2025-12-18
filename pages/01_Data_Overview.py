import pandas as pd
import streamlit as st
import plotly.express as px
from pathlib import Path

st.set_page_config(layout="wide")

st.title("Data Overview")
st.write('''This page is dedicated to providing descriptive statistics and information on the feminists in Wikipedia's 'List of Feminists.'"
This page is brokwn down into three sections - \n
\t1. Pageview Descriptive Statistics\n
\t2. Feminist Frequency and Popularity by Gender\n
\t3. Feminist Frequency and Popularity by Occupation''')

# ---prepare universal data---
ROOT = Path(__file__).resolve().parents[1]
JSON_PATH = ROOT / "data" / "entity_results.jsonl"

info_df = pd.read_json(JSON_PATH,lines=True)

attributes_df = pd.json_normalize(info_df['attributes'])
info_df = info_df.join(attributes_df)

ROOT = Path(__file__).resolve().parents[1]
CSV_PATH = ROOT / "data" / "list_of_feminists.csv"

list_of_feminists = pd.read_csv(CSV_PATH)

pageview_data = pd.read_csv("data/cleaned_pageview_data.csv")

# descriptive statistics for pageviews
st.header('Pageview Descriptive Statistics')
pageview_stats = pageview_data['pageviews'].describe()
st.dataframe(pageview_stats)

st.write('''As seen in the above table, the average number of daily pageviews for feminists on Wikipedia is approximately 1388, with a median of 264.
        This indicates that while some feminists receive a high volume of pageviews, many receive significantly fewer pageviews, as shown by
         the values of the min, 1st and 2nd quartile.''')

# breakdown by feminist gender and occupation
st.header('Feminist Gender Breakdown')

## ---prepare widget for 'sex or gender'---
unique_sex_or_gender = []
for item in info_df['sex or gender']:
    if item not in unique_sex_or_gender and pd.notna(item):
        unique_sex_or_gender.append(item)

selected_sex_or_gender = st.multiselect('Select one or more sexes or genders to compare their presence and popularity on Wikipedia - ', unique_sex_or_gender)

sex_or_gender_selected_info_df = info_df[info_df['sex or gender'].isin(selected_sex_or_gender)]

grouped = sex_or_gender_selected_info_df.groupby("sex or gender")['QID'].count()
sex_or_gender_information_df = grouped.reset_index()
sex_or_gender_information_df.columns = ["Sex or Gender","Count"]
sex_or_gender_information_df.sort_values("Count",ascending=False,inplace=True)

col1, col2 = st.columns([1, 1])

## ---prepare visualizations for 'sex or gender'---
### visualization for sex or gender count
with col1:
    st.dataframe(sex_or_gender_information_df)

with col2:
    st.bar_chart(
        sex_or_gender_information_df,
        x='Sex or Gender',
        y='Count',
        horizontal=False
    )

### visualization for sex or gender pageviews
target_qids = sex_or_gender_selected_info_df.QID

pageviews = [[pageview_data['qid'][index],pageview_data['pageviews'][index]] for index in pageview_data.index if pageview_data['qid'][index] in target_qids.values]
grouped = pd.DataFrame(pageviews,columns=['qid','pageviews']).groupby('qid')['pageviews'].mean()
target_information_df = grouped.reset_index()
target_information_df.columns = ['QID','average_pageviews']

pageview_df = pd.merge(sex_or_gender_selected_info_df, target_information_df, on='QID', how='inner')
pageview_df.sort_values('average_pageviews',ascending=False,inplace=True)
pageview_df['rounded_average_pageviews'] = pageview_df['average_pageviews'].apply(lambda x: round(x))

cleaned_pageview_df = pageview_df[['QID','label','description','sex or gender','occupation','rounded_average_pageviews']]
cleaned_pageview_df.columns = ['QID','Name','Description','Sex or Gender','Occupation','Total Article Pageviews/Day']

with col2:
    st.dataframe(cleaned_pageview_df)

grouped_again = cleaned_pageview_df.groupby('Sex or Gender')['Total Article Pageviews/Day'].mean()
target_information_df_again = grouped_again.reset_index()
target_information_df_again.sort_values('Total Article Pageviews/Day',ascending=False,inplace=True)
target_information_df_again['Average Article Pageviews/Day'] = target_information_df_again['Total Article Pageviews/Day'].apply(lambda x: round(x))

fig = px.pie(cleaned_pageview_df[['Sex or Gender','Total Article Pageviews/Day']],
             values = 'Total Article Pageviews/Day',
             names = 'Sex or Gender')


with col1:
    st.write('Total Proportion of Feminists Present on Wikipedia based on Gender')
    st.plotly_chart(fig, use_container_width=True)

with col1:
    st.write("Average Article Pageviews per Day")
    st.dataframe(target_information_df_again[['Sex or Gender','Average Article Pageviews/Day']])

with col2:
    st.write("Average Article Pageviews per Day")
    st.bar_chart(
    target_information_df_again,
    x='Sex or Gender',
    y='Average Article Pageviews/Day',
    horizontal=False # Set to True for a horizontal orientation
    )

st.write('''As we can see from the information above, female feminists take up the most amount of feminists on Wikipedia's article, 'List of Feminists.' 
         However, as we can also see from the pageview data, the top article based on total pageviews belongs to a male feminist. 
         Out of the top 10 most viewed feminist articles,  only 5 articles belong to female feminists. Adding on, the top average article pageviews
         per day also alines with this trend, where female feminists have the lowest average pageviews per day. However, this may be due to the fact that there are more female feminists, and 
         many female feminist pages get lower pageviews.''')

## ---prepare widget for 'occupation'---

st.header('Feminist Occupation Breakdown')

unique_occupation = []
for item in info_df['occupation']:
    if item not in unique_occupation and pd.notna(item):
        unique_occupation.append(item)
        
selected_occupation = st.multiselect('Select one or more occupations to compare their presence and popularity on Wikipedia - ', unique_occupation)

occupation_selected_info_df = info_df[info_df['occupation'].isin(selected_occupation)]

grouped = occupation_selected_info_df.groupby("occupation")["QID"].count()
occupation_information_df = grouped.reset_index()
occupation_information_df.columns = ["Occupation","Count"]
occupation_information_df.sort_values("Count",ascending=False,inplace=True)

## ---prepare visualizations for 'occupation'---
### visualization for occupation count
col1, col2 = st.columns([1, 1])
st.write("Feminist Count by Occupation")
with col1:
    st.dataframe(occupation_information_df)

with col2:
    st.bar_chart(
    occupation_information_df,
    x='Occupation',
    y='Count',
    horizontal=False # Set to True for a horizontal orientation
    )

### visualization for occupation pageviews
target_qids = occupation_selected_info_df.QID

pageviews = [[pageview_data['qid'][index],pageview_data['pageviews'][index]] for index in pageview_data.index if pageview_data['qid'][index] in target_qids.values]

grouped = pd.DataFrame(pageviews,columns=['qid','pageviews']).groupby('qid')['pageviews'].mean()
target_information_df = grouped.reset_index()
target_information_df.columns = ['QID','average_pageviews']

pageview_df = pd.merge(occupation_selected_info_df, target_information_df, on='QID', how='inner')
pageview_df.sort_values('average_pageviews',ascending=False,inplace=True)
pageview_df['rounded_average_pageviews'] = pageview_df['average_pageviews'].apply(lambda x: round(x))

cleaned_pageview_df = pageview_df[['QID','label','description','sex or gender','occupation','rounded_average_pageviews']]
cleaned_pageview_df.columns = ['QID','Name','Description','Sex or Gender','Occupation','Total Article Pageviews/Day']

with col2:
    st.write("Total Article Pageviews/Day by Occupation")
    st.dataframe(cleaned_pageview_df)

grouped_again = cleaned_pageview_df.groupby('Occupation')['Total Article Pageviews/Day'].mean()
target_information_df_again = grouped_again.reset_index()
target_information_df_again.sort_values('Total Article Pageviews/Day',ascending=False,inplace=True)
target_information_df_again['Average Article Pageviews/Day'] = target_information_df_again['Total Article Pageviews/Day'].apply(lambda x: round(x))

fig = px.pie(cleaned_pageview_df[['Occupation','Total Article Pageviews/Day']],
             values = 'Total Article Pageviews/Day',
             names = 'Occupation')

with col1:
    st.write('Total Proportion of Feminists Present on Wikipedia based on Occupation')
    st.plotly_chart(fig, use_container_width=True)

with col1:
    st.write("Average Article Pageviews per Day by Occupation")
    st.dataframe(target_information_df_again[['Occupation','Average Article Pageviews/Day']])

with col2:
    st.write("Average Article Pageviews per Day by Occupation")
    st.bar_chart(
    target_information_df_again,
    x='Occupation',
    y='Average Article Pageviews/Day',
    horizontal=False # Set to True for a horizontal orientation
    )

st.write('''From the information above, we can see that writers make up a largest portion of feminists on Wikipedia, followed by writers and politicians.
         The top article by pageviews also belongs to a feminist writer. When looking specifically at the average article pageviews per day, we see that occupations
         such as socialite and peace activist are among the top views articles. However, occupations sucha as travelk writer and novelist are also among the top viewed.
         Therefore, the occuption of a feminist may not have a large effect on there popularity.
         ''')

st.write('''From these analyses, we can conclude that gender may play a role in a feminist'[s popularity, especially if the feminist is male. However,
         writing occupations and occupations requiring public interaction and leadership seemlingly contribute to a feminist's popularity, but there is no large difference
         between these two occupations.''')