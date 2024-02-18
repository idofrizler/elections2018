import pandas as pd
import streamlit as st
import altair as alt

# Load spreadsheet
xl = pd.ExcelFile('full-list.xlsx')

# Load a sheet into a DataFrame by its name
df = xl.parse('DataSheet')

# rename column "שם ישוב" to "city"
df = df.rename(columns={"שם ישוב": "city"})
df = df.rename(columns={"כינוי": "party"})
df = df.rename(columns={"אותיות": "letters"})
df = df.rename(columns={"שם": "name"})
df = df.rename(columns={"מין": "gender"})
df = df.rename(columns={"מס' סידורי": "index"})

# remove columns "מנדטים" and "אותיות"
df = df.drop(columns=["מנדטים"])

# count candidates by city
df['count'] = df.groupby('city')['city'].transform('count')

# count candidates by city and letters
df['count_letters'] = df.groupby(['city', 'letters'])['city'].transform('count')

df['count_gender'] = df.groupby(['city', 'gender'])['city'].transform('count')

# keep only one record per city, letters
agg_df_1 = df.drop_duplicates(subset=['city', 'letters'])

agg_df_2 = df.drop_duplicates(subset=['city', 'gender'])

# plot the aggregated data using streamlit
st.title('Municipal election results 2018')

# Checkbox for expanding rows
expand_rows = st.checkbox('Expand Rows', False)

# Display first 20 cities or all cities based on checkbox state
if expand_rows:
    displayed_df = agg_df_1
else:
    # filter only top 20 cities by count
    displayed_df = agg_df_1[agg_df_1['count'] > 20]

# plot the aggregated data using altair (sorted bar chart)
st.header('Number of representatives by city')
c = alt.Chart(displayed_df).mark_bar().encode(
    x=alt.X('count_letters', title='Number of representatives'),  # Set axis format to display as integers
    y=alt.Y('city', sort='-x'),
    color='letters'
)
st.altair_chart(c, use_container_width=True)


# show a pie chart by party (top 20 parties)
st.header('Number of representatives by party')
party_df = df.groupby('letters').size().reset_index(name='count')
party_df = party_df.sort_values('count', ascending=False)

if expand_rows:
    party_df = party_df
else:
    # filter only top 20 cities by count
    party_df = party_df.head(20)

c = alt.Chart(party_df).mark_bar().encode(
    x=alt.X('count', title='Number of representatives'),
    y=alt.Y('letters', sort='-x'),
    color='letters'
)
st.altair_chart(c, use_container_width=True)


# Display first 20 cities or all cities based on checkbox state
if expand_rows:
    displayed_df_2 = agg_df_2
else:
    # filter only top 20 cities by count
    displayed_df_2 = agg_df_2[agg_df_2['count'] > 20]

st.header('Gender division by city')
c = alt.Chart(displayed_df_2).mark_bar().encode(
    x=alt.X('count_gender', title='Number of representatives'),
    y=alt.Y('city', sort='-x'),
    color=alt.Color('gender', scale=alt.Scale(domain=['ז', 'נ'], range=['blue', 'pink']))
)
st.altair_chart(c, use_container_width=True)



# show a pie chart of all female candidates by city
female_df = df[df['gender'] == 'נ']
female_city_df = female_df.groupby('city').size().reset_index(name='count')

if expand_rows:
    female_city_df = female_city_df
else:
    # filter only top 20 cities by count
    female_city_df = female_city_df.head(20)

st.header('Female representatives by city')

c = alt.Chart(female_city_df).mark_bar().encode(
    x=alt.X('count', title='Number of female representatives'),
    y=alt.Y('city', sort='-x')
)
st.altair_chart(c, use_container_width=True)

