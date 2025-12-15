import streamlit as st
import pandas as pd
import seaborn as sns
import plotly.express as px
from sklearn.metrics import confusion_matrix
from sklearn.metrics import accuracy_score, confusion_matrix
import matplotlib.pyplot as plt

st.set_page_config(layout="wide")

st.title("Text Classification Analysis")
st.write('''This page is dedicating to text classification to solve my fourth research question. We've already looked at the influence of a feminist's occupation
         on the 'Data Overview' page, but what about the nature of their occupation? For this analysis, I hand-labeled 100 feminists based on their occupation into 
         one of three categories: Category 1 - scholars, artists, authors and feminists have dedicated their livihood to art or an academic discipline, Category 2 
         - organizers, politicians, public figures, and feminists who act as figureheads and leaders for campaigns and moblization, or Category 3 - if a feminist 
         falls into both of the previous categories. I then trained my Naive Bayes model on this data, and used the labels assigned by the model for the next 700 entries.
         In order to evaluation the accuracy of the model, I also hand labeled the next 100 entries and compare my hand-labeling to the model's labeling of these 100 feminists.
         This page is split into three categories surrouding my text classification analysis.
         - \n
         \t1. Text Classification Training \n
         \t2. Naive Bayes Accuracy \n
         \t3. Text Classification Results''')

# preparing universal data
text_classification_predictions = pd.read_csv("data/text_classification_predictions.csv")
hand_classified_predictions = text_classification_predictions[:101]

training_data = pd.read_csv("data/feminist_article_summaries.csv")

pageview_data = pd.read_csv("data/cleaned_pageview_data.csv")

# stats for original training data
training_data_grouped = training_data.groupby('label')['qid'].count()
training_data_df = training_data_grouped.reset_index()
training_data_df.columns = ['Assigned Label','Count']
training_data_df.loc[3] = {'Assigned Label': 'Total','Count':sum(list(training_data_df['Count']))}

st.header("Text Classification Training")
st.write("The dataframe below shows the statistics of the training data that was used to train the bayes net for my three categories.")
st.dataframe(training_data_df)

# model accuracy analysis
col1, col2 = st.columns([1, 1])
## ---preparing data for analysis---
assigned_labels_grouped = hand_classified_predictions.groupby('assigned_label')['qid'].count()
assigned_labels_df = assigned_labels_grouped.reset_index()
assigned_labels_df.columns = ['Assigned Label','Count']
assigned_labels_df.loc[3] = {'Assigned Label': 'Total','Count':sum(list(assigned_labels_df['Count']))}

with col1:
    st.write("Hand-assigned Label Statistics for Accuracy Analysis")
    st.dataframe(assigned_labels_df)

predicted_labels_grouped = hand_classified_predictions.groupby('predicted_label')['qid'].count()
predicted_labels_df = predicted_labels_grouped.reset_index()
predicted_labels_df.columns = ['Predicted Label','Count']
predicted_labels_df.loc[3] = {'Predicted Label': 'Total','Count':sum(list(predicted_labels_df['Count']))}
with col2:
    st.write("Naive Bayes Label Statistics for Accuracy Analysis")
    st.dataframe(predicted_labels_df)

bar_chart_df = pd.DataFrame({'label_type':['Assigned Label']*3+['Predicted Label']*3,
                             'label_value':[1,2,3]*2,
                             'count':list(assigned_labels_df['Count'])[:3]+list(predicted_labels_df['Count'])[:3]})

## ---generating bar chart---
fig = px.bar(bar_chart_df, 
            x='label_value', 
            y='count',
            color='label_type',
            barmode="group")

st.write('Number of Labels in Each Category Assigned by Me and Predicted by Bayes Model')
st.plotly_chart(fig, use_container_width=True)

## ---generating confusion matrix---
st.header("Naive Bayes Accuracy")

accuracy = accuracy_score(hand_classified_predictions["assigned_label"], hand_classified_predictions["predicted_label"])
st.write(f"The following is a confusion matrix showing the labels assigned by me (True Labels) and assigned by the Bayes model (Predicted Labels). Model Accuracy : {str(round(accuracy,3)*100)}+'%")

cm = confusion_matrix(hand_classified_predictions["assigned_label"], hand_classified_predictions["predicted_label"])

fig, ax = plt.subplots(figsize=(4, 4))
    
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues',ax=ax)
    
ax.set_xlabel('Predicted Labels')
ax.set_ylabel('True Labels')
ax.set_xticklabels([1,2,3])
ax.set_yticklabels([1,2,3])

st.pyplot(fig)

# using text classification for feminist breakdown
## --- preparing data for analysis---
all_text_classification = pd.concat([training_data,text_classification_predictions])
all_text_classification = all_text_classification[(all_text_classification['label'].notna()) | (all_text_classification['predicted_label'].notna())]

grouped = pageview_data.groupby(['date_object','qid'])['pageviews'].mean()
pageview_info = grouped.reset_index()

merged = pd.merge(all_text_classification,pageview_info,on='qid')

merged["universal_label"] = [label for label in list(merged['label']) if pd.notna(label)]+[label for label in list(merged['predicted_label']) if pd.notna(label)]
merged.sort_values('date_object',inplace=True)

grouped_again_means = merged.groupby(['date_object','universal_label'])['pageviews'].mean()
final_merged_means = grouped_again_means.reset_index()

st.header("Text Classification Results")

selected_analysis = st.selectbox('Select an analysis to get started -',['Total Pageviews','Average Pageviews'])

if selected_analysis == 'Average Pageviews':
    fig = px.line(
        final_merged_means,
        x='date_object',
        y="pageviews",
        color='universal_label',
        title="Average Pageviews of Articles based on Wave of Feminism Over 7 Day Period",
        markers=True
        )

    st.plotly_chart(fig, use_container_width=True)

else:
    grouped_again_sum = merged.groupby(['date_object','universal_label'])['pageviews'].sum()
    final_merged_sum = grouped_again_sum.reset_index()

    fig = px.line(
        final_merged_sum,
        x='date_object',
        y="pageviews",
        color='universal_label',
        title="Total Pageviews of Articles based on Wave of Feminism Over 7 Day Period",
        markers=True
        )

    st.plotly_chart(fig, use_container_width=True)