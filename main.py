import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import seaborn as sns
import numpy as np
import seaborn as sns


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
def plot_prize_per_year():
    #count how many prizes were awarded evry year
    df_clean_year=df['year'].value_counts()
    df_clean_year=df_clean_year.sort_index()
    #Create a 5 year rolling average of the number of prizes 
    moving_av_value=df_clean_year.rolling(window=5).mean()
    # Generate tick values for every 5 years from 1900 to 2020
    plt.figure(figsize=(8, 4), dpi=110)
    plt.title('Number of Nobel Prizes Awarded per Year', fontsize=18)
    plt.yticks(fontsize=14)
    plt.xticks(ticks=np.arange(1900, 2021, step=5), 
            rotation=45)
    
    ax = plt.gca() # get current axis
    ax.set_xlim(1900, 2020)
    ax.scatter(x=df_clean_year.index, 
            y=df_clean_year.values, 
            c='dodgerblue', )
    
    ax.plot(df_clean_year.index, 
            moving_av_value.values, 
            c='crimson', 
            )
def plot_prize_avarage():
    df_clean_year=df['year'].value_counts()
    moving_av_value=df_clean_year.rolling(window=5).mean()
    #Calculate the average prize share of the winners on a year by year basis.
    df_avarage_year= df.groupby('year', as_index=False).agg({'share_pct':pd.Series.mean})
    share_moving_average=df_avarage_year.rolling(window=5).mean()
    #Create a line chart showing the average share of the winners on a year by year basis.
    plt.figure(figsize=(8, 4), dpi=110)
    plt.title('Number of Nobel Prizes Awarded per Year', fontsize=18)
    plt.yticks(fontsize=14)
    plt.xticks(ticks=np.arange(1900, 2021, step=5), 
            rotation=45)
    
    ax1 = plt.gca() # get current axis
    ax2=ax1.twinx()
    ax1.set_xlim(1900, 2020)
    ax1.scatter(x=df_clean_year.index, 
            y=df_clean_year.values, 
            c='dodgerblue', )
    
    ax1.plot(df_clean_year.index, 
            moving_av_value.values, 
            c='crimson', 
            )
    #plot the share_pct
    ax2.plot(df_avarage_year.year,
            share_moving_average.share_pct,
            c='black',)
    plt.savefig('images/num_prizes_awarded_year.png')
top_countries = df.groupby(['birth_country_current'], 
                                  as_index=False).agg({'prize': pd.Series.count})
 
top_countries.sort_values(by='prize', inplace=True)
top20_countries = top_countries[-20:]
#create a top 20 countries that awarded the prizes
cat_country = df.groupby(['birth_country_current', 'category'], 
                               as_index=False).agg({'prize': pd.Series.count})
cat_country.sort_values(by='prize', ascending=False, inplace=True)
merged_df = pd.merge(cat_country, top20_countries, on='birth_country_current')
# change column names
merged_df.columns = ['birth_country_current', 'category', 'cat_prize', 'total_prize'] 
merged_df.sort_values(by='total_prize', inplace=True)
def plot_top20_countries():
    cat_cntry_bar = px.bar(x=merged_df.cat_prize,
                        y=merged_df.birth_country_current,
                        color=merged_df.category,
                        orientation='h',
                        title='Top 20 Countries by Number of Prizes and Category')
    
    cat_cntry_bar.update_layout(xaxis_title='Number of Prizes', 
                                yaxis_title='Country')
    cat_cntry_bar.write_image('images/top20_countries.png')
    cat_cntry_bar.show()
#create new dataframe that take the location with birth_country_current
df_countries = df.groupby(['birth_country_current', 'ISO'], 
                               as_index=False).agg({'prize': pd.Series.count})
df_countries.sort_values('prize', ascending=False)
#plot the map by plotly
def plot_map():
    world_map = px.choropleth(df_countries,
                            locations='ISO',
                            color='prize', 
                            hover_name='birth_country_current', 
                            color_continuous_scale=px.colors.sequential.matter)
    
    world_map.update_layout(coloraxis_showscale=True,)
    world_map.update_layout(
        title_text='Nobel Prizes Awarded by Country',
        title_x=0.5,
        title_font=dict(size=24),
    )
    world_map.write_image('images/world_map.png')
    world_map.show()
#total number of prizes awarded changed over the years.
prize_by_year = df.groupby(by=['birth_country_current', 'year'], as_index=False).count()
prize_by_year = prize_by_year.sort_values('year')[['year', 'birth_country_current', 'prize']]
#reate a series that has the cumulative sum for the number of prizes won.
cumulative_prizes = prize_by_year.groupby(by=['birth_country_current',
                                              'year']).sum().groupby(level=[0]).cumsum()
cumulative_prizes.reset_index(inplace=True)
#plot the line chart
def plot_line():
    plt.figure(figsize=(8, 4), dpi=110)
    line_chart = px.line(cumulative_prizes,
                        x='year',
                        y='prize',
                        color='birth_country_current',
                        title='Cumulative Number of Prizes Awarded by Country')

    line_chart.update_layout(xaxis_title='Year',
                             xaxis_range=[1901, 2020],
                            yaxis_title='Number of Prizes')
    line_chart.write_image('images/lines_chart.png')
    line_chart.show()
#organisations affiliated with the Nobel laureates
orgs = df.groupby(['organization_name'],
                    as_index=False).agg({'prize': pd.Series.count})
orgs.sort_values(by='prize', inplace=True)
orgs_top20 = orgs[-20:]
def plot_orgs():
    orgs_bar = px.bar(orgs_top20,
                    x=orgs_top20.prize,
                    y=orgs_top20.organization_name,
                    orientation='h',
                    color=orgs_top20.prize,
                    title='Top 20 Organizations by Number of Prizes')

    orgs_bar.update_layout(xaxis_title='Number of Prizes',
                            yaxis_title='Organization')
    orgs_bar.write_image('images/orgs_bar.png')
    orgs_bar.show()
#top 20 oragnizations cities
orgs_city = df.groupby(['organization_city'],
                        as_index=False).agg({'prize': pd.Series.count})
orgs_city.sort_values(by='prize', inplace=True)
orgs_city_top20 = orgs_city[-20:]
def plot_orgs_city():
    orgs_city_bar = px.bar(orgs_city_top20,
                            x=orgs_city_top20.prize,
                            y=orgs_city_top20.organization_city,
                            orientation='h',
                            color=orgs_city_top20.prize,
                            title='Top 20 Organization Cities by Number of Prizes')

    orgs_city_bar.update_layout(xaxis_title='Number of Prizes',
                                yaxis_title='Organization City')
    orgs_city_bar.write_image('images/orgs_city_bar.png')
    orgs_city_bar.show()
#Create a plotly bar chart graphing the top 20 birth cities of Nobel laureates
birth_city = df.groupby(['birth_city'],
                        as_index=False).agg({'prize': pd.Series.count})

birth_city.sort_values(by='prize', inplace=True)
birth_city_top20 = birth_city[-20:]
def plot_birth_city():
    birth_city_bar = px.bar(birth_city_top20,
                            x=birth_city_top20.prize,
                            y=birth_city_top20.birth_city,
                            orientation='h',
                            color=birth_city_top20.prize,
                            title='Top 20 Birth Cities by Number of Prizes')

    birth_city_bar.update_layout(xaxis_title='Number of Prizes',
                                yaxis_title='Birth City')
    birth_city_bar.write_image('images/birth_city_bar.png')
    birth_city_bar.show()
#create a new dataframe of organization country and city and name with prize
country_city_org = df.groupby(by=['organization_country', 
                                       'organization_city', 
                                       'organization_name'], as_index=False).agg({'prize': pd.Series.count})

country_city_org.sort_values(by='prize', ascending=False, inplace=True)
#create the sunburst chart
def plot_sunburst():
    sunburst_chart = px.sunburst(country_city_org,
                                path=['organization_country',
                                    'organization_city',
                                    'organization_name'],
                                values='prize',
                                color='prize',
                                color_continuous_scale='RdBu',
                                title='Organizations by Country, City, and Name')
    sunburst_chart.update_layout(coloraxis_showscale=True)
    sunburst_chart.show()

#calculate the age of laureate in the year of the ceremony
df['winnig_age']=(df['year']-df['birth_date'].dt.year)
#the oldest winner's age
oldest_winner_age=df['winnig_age'].max()
#the youngest winner's age
youngest_winner_age=df['winnig_age'].min()
#the name of oldest winner
oldest_winner_name=df[df['winnig_age']==oldest_winner_age]['full_name'].values[0]
print(f"Oldest winner is {oldest_winner_name} of age {oldest_winner_age}")
#the name of youngest winner
youngest_winner_name=df[df['winnig_age']==youngest_winner_age]['full_name'].values[0]
print(f"Youngest winner is {youngest_winner_name} of age {youngest_winner_age}")
#the category of oldest winner
oldest_winner_category=df[df['winnig_age']==oldest_winner_age]['category'].values[0]
print(f"Oldest winner category is {oldest_winner_category}")
#the category of youngest winner
youngest_winner_category=df[df['winnig_age']==youngest_winner_age]['category'].values[0]
print(f"Youngest winner category is {youngest_winner_category}")
#get the 75% of winner are younger than
age_75_percentile=df['winnig_age'].quantile(0.75)
print(f"there are 75% of winner are younger than {age_75_percentile}")
#create a histogram of the age of the winners using seaborn
def plot_age_histogram():
    plt.figure(figsize=(8, 4), dpi=110)
    sns.histplot(data=df,
                x='winnig_age',
                bins=30,
                kde=True,
                color='blue')
    plt.title('Age of Nobel Prize Winners', fontsize=18)
    plt.xlabel('Age', fontsize=14)
    plt.ylabel('Number of Winners', fontsize=14)
    plt.savefig('images/age_histogram.png')
    plt.show()
#create a regplot by seaborn to see that if the age of laureates increase or decrease
def plot_age_regplot():
    plt.figure(figsize=(10, 4), dpi=115)
    sns.regplot(data=df,
                x='year',
                y='winnig_age',
                lowess=True,
                scatter_kws={'alpha': 0.4},
                line_kws={'color': 'red'})
    plt.title('Age of Nobel Prize Winners Over Time', fontsize=18)
    plt.xlabel('Year', fontsize=14)
    plt.ylabel('Age', fontsize=14)
    plt.savefig('images/age_regplot.png')
    plt.show()

#use seaborn to create boxplot to see the distribution of the age of the winners
def plot_age_boxplot():
    plt.figure(figsize=(8, 4), dpi=110)
    sns.boxplot(data=df,
                x='category',
                y='winnig_age',
                color='green')
    plt.title('Distribution of Age by Category', fontsize=18)
    plt.xlabel('Category', fontsize=14)
    plt.ylabel('Age', fontsize=14)
    plt.savefig('images/age_boxplot.png')
    plt.show()

#use lmplot to create 6 separate plots for the age of the winners by category
def plot_age_category():
    plt.figure(figsize=(8, 6), dpi=110)
    sns.lmplot(data=df,
            x='year',
            y='winnig_age',
            hue='category',
            lowess=True,)
    plt.title('Age of Nobel Prize Winners Over Time by Category', fontsize=18)
    plt.xlabel('Year', fontsize=14)
    plt.ylabel('Age', fontsize=14)
    plt.savefig('images/age_category.png')
    plt.show()
plot_age_category()
plot_age_boxplot()
plot_age_regplot()
plot_age_histogram()
plot_sunburst()
plot_birth_city()
plot_orgs_city()
plot_orgs()
plot_prize_avarage()
plot_line()
plot_top20_countries()
plot_prize_per_year()
plot_map()
v_bar.show()
fig.show()
