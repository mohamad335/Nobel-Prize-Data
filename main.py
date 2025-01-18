import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import seaborn as sns
import numpy as np

df=pd.read_csv('data/nobel_prize_data.csv')
#convert birth_date column to panda datetime
df['birth_date']=pd.to_datetime(df['birth_date'])
#add a column called shard_pct which has the laureates' share as a percentage in the form of a floating-point number.
separated_values = df.prize_share.str.split('/', expand=True)
numerator = pd.to_numeric(separated_values[0])
denomenator = pd.to_numeric(separated_values[1])
df['share_pct'] = numerator / denomenator
#create a donut chart for prizes went to men compared to how many prizes went to women
df_men= df[df['sex']== 'Male']
df_women=df[df['sex']=='Female']
#calculate the prisez for men and women
prize_men=df_men.shape[0]
prize_women=df_women.shape[0]
#calculate the percentage of prizes that went to women
total_prizes= prize_men + prize_women
percentage_women = (prize_women/total_prizes)*100
#create a donut chart using plotly
fig = px.pie(
    names=['Men','Female'],
    values=[prize_men,prize_women],
    hole=0.3,
    title='Nobel prizes: Men Vs Women'
)
#the first three women to win
first_thrd_women = df_women['full_name'].head(3)
#check if there any people received a nobel prizes more than one
winners=df['full_name'].value_counts()
winners=winners[winners>1]
print(f"People who received a Nobel Prize more than once:{winners}")
catagories = df['category'].value_counts()
print(f"Catagories of nobel prizes:{catagories}")
#create a chart bar using plotly with the number of prizes awarded by category.
v_bar=px.bar(
    x=catagories.index,
    y=catagories.values,
    title='Nobel prizes by category',
    color = catagories.values,
    color_continuous_scale='Aggrnyl'
)
v_bar.update_layout(
    xaxis_title='Category',
    coloraxis_showscale=False,
    yaxis_title='Number of prizes'
)
v_bar.write_image('images/num_prizes_awarded.png')
#first prize in the field of economics awarded
first_econ = df[df['category']=='Economics']['year'].min()
name_first_econ = df[df['year']==first_econ]['full_name'].values[0]
print(f"First prize in the field of economics awarded is:{name_first_econ}")
#create a chart bar that shows the split between men and women by category.
category_men_women=df.groupby(['category','sex'],as_index=False).agg({'prize':pd.Series.count})
#we need to sort the value to put the value of women on top of bar chart because it only 6.5%
category_men_women.sort_values('prize',ascending=False,inplace=True)
v_bar_split=px.bar(x=category_men_women.category,
                   y=category_men_women.prize,
                   color=category_men_women.sex,
                   title="Number Of Prizes Awarded Per Caregory Split")
v_bar_split.update_layout(xaxis_title='Category'
                          ,yaxis_title='Number of Prizes')
v_bar_split.write_image('images/num_prizes_awarded_split.png')
v_bar_split.show()


