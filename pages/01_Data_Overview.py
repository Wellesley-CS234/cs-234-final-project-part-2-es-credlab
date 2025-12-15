import pandas as pd
import streamlit as st
import plotly.express as px

st.set_page_config(layout="wide")

st.title("Data Overview")
st.write('''This page is dedicated to providing descriptive statistics and information on the feminists in Wikipedia's 'List of Feminists.'"
This page is brokwn down into three sections - \n
\t1. Pageview Descriptive Statistics\n
\t2. Feminist Frequency and Popularity by Gender\n
\t3. Feminist Frequency and Popularity by Occupation''')
st.header('Feminist Gender Breakdown')
# ---prepare universal data---
info_df = pd.read_json("data\entity_results.jsonl",lines=True)

attributes_df = pd.json_normalize(info_df['attributes'])
info_df = info_df.join(attributes_df)

list_of_feminists = pd.read_csv("data\list_of_feminists.csv")
pageview_data = pd.read_csv("data\cleaned_pageview_data.csv")

# breakdown by feminist gender and occupation
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
    st.plotly_chart(fig, use_container_width=True)

with col1:
    st.dataframe(target_information_df_again[['Sex or Gender','Average Article Pageviews/Day']])

with col2:
    st.bar_chart(
    target_information_df_again,
    x='Sex or Gender',
    y='Average Article Pageviews/Day',
    horizontal=False # Set to True for a horizontal orientation
    )

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
    st.dataframe(cleaned_pageview_df)

grouped_again = cleaned_pageview_df.groupby('Occupation')['Total Article Pageviews/Day'].mean()
target_information_df_again = grouped_again.reset_index()
target_information_df_again.sort_values('Total Article Pageviews/Day',ascending=False,inplace=True)
target_information_df_again['Average Article Pageviews/Day'] = target_information_df_again['Total Article Pageviews/Day'].apply(lambda x: round(x))

fig = px.pie(cleaned_pageview_df[['Occupation','Total Article Pageviews/Day']],
             values = 'Total Article Pageviews/Day',
             names = 'Occupation')

with col1:
    st.plotly_chart(fig, use_container_width=True)

with col1:
    st.dataframe(target_information_df_again[['Occupation','Average Article Pageviews/Day']])

with col2:
    st.bar_chart(
    target_information_df_again,
    x='Occupation',
    y='Average Article Pageviews/Day',
    horizontal=False # Set to True for a horizontal orientation
    )