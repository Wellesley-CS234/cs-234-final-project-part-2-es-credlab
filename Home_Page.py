import streamlit as st

st.set_page_config(page_title="Multi-Page App Demo")
st.title("Welcome to the Home Page")

st.header("1. Introduction")
st.write('''Across the world, women have worked tirelessly for thousands of years to fight for the same rights that are unfairly 
         given to men. Feminists - defined as 'an advocate of women's rights on the basis of the equality of the sexes' according
         to Oxford Languages - advocate for equal rights through different medias, mediums, and strategies. These stratigies can include
         writing fiction novels, creating essays, organizing protests (peaceful or otherwise), campiagning for office, building
         organizations, and so much more. Through this analysis, I hope to discover which mediums of feminism are the most effective.
         Are feminist authors more well known than feminist politicians? Are feminist organizers more influencial or memorable than 
         feminist artists? What contributes to a feminist's popularity and the ability for their ideas to spread? These questions 
         give rise to my research questions, were through this analysis, I aim to answer the following -\n
         \t1. Does the gender or occupation of a feminist seemingly influence to their popularity?\n
         \t2. Does a feminist's country of origin seemingly influence their popularity?\n
         \t3. Does the wave of feminism that a feminist is associated with seemingly influence their popularity?\n
         \t4. Are feminist scholars and authors more well known than feminist organizers and public figures?\n
         ''')
st.write('''I hypothesize that authors and writers will be the most well known on Wikipedia. I believe organizers and public figures 
         from the past will be less well known.''')

st.header("2. Data Summary")
st.write('''For this analysis, I will be working with the Wikipedia 2024 DPDP Dataset. Using this dataset, I will use average and total 
         pageviews over the first seven days in January, 2024 to gauge a feminist's popularity based on the amount of views their associated
         Wikipedia article recieves. Descriptive statistics and more data information is aviable on the 'Data Overview' page of this streamlit.''')

st.header("3. New Features")
st.write('''I will be utilizing the provided Wikidata attributes for Wikipedia articles to help answer my first research question. The specific 
         labels I will be looking into are 'sex and gender' and 'occupation.''')
st.write('''I will be creating my own classification categories to train a Naive Bayes model for text classification. The details of my original
         classifiers are avaiable in the 'Text Classification' section of this page, and also on the 'Text Classification' page on this streamlit.''')

st.header("4. Text Classification")
st.write('''I will be using three classifiers to train my Naive Bayes Text Classification model: 1. scholars, artists, authors and feminists 
         have dedicated their livihood to art or an academic discipline, 2. organizers, politicians, public figures, and feminists who 
         act as figureheads and leaders for campaigns and moblization, and 3. feminists who fall into both categories. See the results of this text 
         classification analysis on the 'Text Classification' page.''')

st.header('''Click on a page in the sidebar to navigate.''')
