
import streamlit as st
#import filetype
import numpy as np
from io import StringIO
import pandas as pd
import matplotlib.pyplot as plt
#import seaborn as sns
import altair as alt
import plotly.express as px
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
st.title('GeoAnalytics Platform')
def preprocesing(file):
    df=pd.read_csv(file)
    #df.head(5)
    #df.column.fillna(0,inplace=True)
    return df

def plot_net_conv(scope,title,file):
    df=preprocesing(file)
    fig = px.choropleth(
    df,
    locations ="Code",
    color ="Net forest conversion",
    hover_name ="Entity",
    scope=scope,
    color_continuous_scale='RdYlGn',
    animation_frame ="Year")
 
    fig.update_layout(title_text=title,
    font_family="Rockwell",
    title_font_size=20,
    coloraxis_colorbar=dict(
    title='Net Forest Conversion'))
 
    #fig.show()
    return fig
def plot_net_for_Internetuses(scope,title,file):
    df=preprocesing(file)
    fig = px.choropleth(
    df,
    locations ="Code",
    color ="Fixed broadband subscriptions (per 100 people)",
    hover_name ="Entity",
    scope=scope,
    color_continuous_scale='RdYlGn',
    animation_frame ="Year")
 
    fig.update_layout(title_text=title,
    font_family="Rockwell",
    title_font_size=20,
    coloraxis_colorbar=dict(
    title='Internet Usage'))
 
    #fig.show()
    return fig
def plot_net_for_auto_GAP(scope,title,df,option):
    #df=preprocesing(file)
    fig = px.choropleth(
    df,
    locations ="Code",
    color =option,
    hover_name ="Entity",
    scope=scope,
    color_continuous_scale='RdYlGn',
    animation_frame ="Year")
 
    fig.update_layout(title_text=title,
    font_family="Rockwell",
    title_font_size=20,
    coloraxis_colorbar=dict(
    title='Usage'))
 
    #fig.show()
    return fig
    
def model_train(file,name_of_training_column1,name_of_training_column2,name_of_training_column_Y):
    df=preprocesing(file)
    x1 = df.drop([name_of_training_column1,name_of_training_column2,'Code'], axis=1)
    y1 = df[name_of_training_column1]
    model=LinearRegression()
    model.fit(x1,y1)
    #print("Coefficient: ",model.coef_)
    #print("intercept: ",model.intercept_)
    pre = model.predict(x1)
    return model

def prediction(file,name_of_training_column1,name_of_training_column2,name_of_training_column_Y,list_years):

    model=model_train(file,name_of_training_column1,name_of_training_column2,name_of_training_column_Y)
    for i in list_years:
        return model.predict([[i]])

def auto_prediction(x1,y1,list_years):
    #list_years=list(map(int,input("\nEnter the years : ").strip().split()))
    #file=input('input file name')
    #df=preprocesing(file)
    model=LinearRegression()
    model.fit(x1,y1)
    model.predict(x1)
    #model=model_train(file,name_of_training_column1,name_of_training_column2,name_of_training_column_Y)
    for i in list_years:
        return model.predict([[i]])

def main():
    menu = ["Home", "annual changes in forest area", "Internet Usage across the world","Auto GeoAnalytics","About"]
    choice = st.sidebar.selectbox("Menu",menu)
    if choice == "Home":
        st.info("Innovation is the only way to win")
        primaryColor="#F63366"
        backgroundColor="#FFFFFF"
        secondaryBackgroundColor="#F0F2F6"
        textColor="#262730"
        font="sans serif"
    if choice=="annual changes in forest area":
        #list_years = [2022, 2023, 2024, 2025, 2026,2027, 2028,2029,2030]
        list_years=st.multiselect("Please select numbers", [2022, 2023, 2024, 2025, 2026,2027, 2028,2029,2030])
        st.write(list_years)
        
        if st.button("Process"):
            file = 'https://raw.githubusercontent.com/avanishsingh07/GeoAnalytics_Platform/main/annual-change-forest-area.csv'
            st.plotly_chart(plot_net_conv('world','Net Forest Conversion across the world',file), use_container_width=True)
            dataframe = pd.read_csv(file)
            st.write(dataframe.head(5))
            name_of_training_column1='Net forest conversion'
            name_of_training_column2='Entity'
            name_of_training_column_Y='Net forest conversion'
            pred=prediction(file,name_of_training_column1,name_of_training_column2,name_of_training_column_Y,list_years)
            for i in pred:
                
                st.write(i)
    elif choice=="Internet Usage across the world":
        #list_years = [2022, 2023, 2024, 2025, 2026,2027, 2028,2029,2030]
        list_years=st.multiselect("Please select numbers", [2022, 2023, 2024, 2025, 2026,2027, 2028,2029,2030])
        st.write(list_years)
        
        if st.button("Process"):
            file = 'https://raw.githubusercontent.com/avanishsingh07/GeoAnalytics_Platform/main/broadband-penetration-by-country.csv'
            st.plotly_chart(plot_net_for_Internetuses('world','Internet Usage across the world',file), use_container_width=True)
            dataframe = pd.read_csv(file)
            st.write(dataframe.head(5))
            name_of_training_column1='Fixed broadband subscriptions (per 100 people)'
            name_of_training_column2='Entity'
            name_of_training_column_Y='Fixed broadband subscriptions (per 100 people)'
            pred=prediction(file,name_of_training_column1,name_of_training_column2,name_of_training_column_Y,list_years)
            for i in pred:
                
                st.write(i)
    elif choice=="Auto GeoAnalytics":
        uploaded_file = st.file_uploader("Choose a file")
        if uploaded_file is not None:
     # To read file as bytes:
            bytes_data = uploaded_file.getvalue()
            #st.write(bytes_data)

     # To convert to a string based IO:
            stringio = StringIO(uploaded_file.getvalue().decode("utf-8"))
            #st.write(stringio)

     # To read file as string:
            string_data = stringio.read()
            #st.write(string_data)

     # Can be used wherever a "file-like" object is accepted:
            dataframe = pd.read_csv(uploaded_file)
            st.write(dataframe.head(5))
            cl1=str(dataframe.columns)
            st.write(cl1)
            area = alt.Chart(dataframe).mark_area(color="maroon").encode(x=dataframe.columns[0], y=dataframe.columns[3])
            st.altair_chart(area)
            scatter  = alt.Chart(dataframe).mark_point().encode(x=dataframe.columns[2], y=dataframe.columns[3]).interactive()
            st.altair_chart(scatter)
            scope='world'
            title=uploaded_file.name
            option=dataframe.columns[3]
            if st.button("Next"):
                st.plotly_chart(plot_net_for_auto_GAP(scope,title,dataframe,option))
        #df=preprocesing(uploaded_file)
            #st.write("Drop non-numerical/non-x1_features column from dataset")
            #selected_option=st.multiselect('Please select all possible columns',cl1)
                
    else:
        st.subheader("About")
        st.text("Quotes by Avanish")
        st.info("When your models work efficently, It's hot as Fuck...")
        font="monospace"
        st.subheader('created by AVANISH')
        st.write("contact on [Instagram](https://www.instagram.com/i.m_avanish/)")
        st.write("contact on [GitHub](https://github.com/avanishsingh07)")
        st.write("contact on [LinkedIn](https://www.linkedin.com/in/avanish-singh-763aa81b2/)")
        st.info("Phone No.:- 7800105545")
        st.text("work in progress")
if __name__ == '__main__':
    main()
