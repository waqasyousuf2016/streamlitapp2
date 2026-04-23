# 
import streamlit as st
import pandas as pd
import plotly.express as px
from streamlit_option_menu import option_menu # This opion is used for navbar.


st.set_page_config(layout="wide")

#---------------- Load data-----------

df=pd.read_csv("cgeiNf.csv")

#------------- NavBar-----------
select = option_menu(
    menu_title=None,
    options=["Home","Player Analysis","Country Insights","Comparison","Data Explorer"],
    icons=["house","person","globe","bar-chart","table"],
    orientation="horizontal"
)

#--------------- Home---------------------

if select == "Home":
    st.title="Cricket Analysis Dashboard"

    col1,col2,col3 = st.columns(3)

    col1.metric("Total Player",df["Player"].nunique())

    col2.metric("Total Runs",df["Runs"].sum())

    col3.metric("Countries",df["Country"].nunique())

    st.dataframe(df.head())


#-------------- Player Analysis-----------------

elif select=="Player Analysis":
    st.title="Player Analysis"

    player = st.selectbox("Select Player",df["Player"])

    pdata = df[df["Player"]==player]

    stats = ["100","50","4s","6s"]
    chart_data = (pdata[stats].iloc[0].reset_index())# iloc[0]
    chart_data.columns = ["stats","Value"]

    fig=px.bar(
        chart_data,
        x="Value",
        y="stats",
        title="Player Performances"
    )

    st.plotly_chart(fig,use_container_width=True)


#------------------ Country Insight--------------------

elif select=="Country Insights":
    st.title="Country Insights"

    country = st.selectbox("Select Country",df["Country"])

    col1,col2,col3,col4 = st.columns(4)

    cdata = df[df["Country"]==country]

    player = cdata["Player"].nunique()
    total_runs = cdata["Runs"].sum()
    total_matches = cdata["Matches"].sum()
    total_innings = cdata["innings"].sum()

    col1.metric("Total Player",player)
    col2.metric("Total Runs",total_runs)
    col3.metric("Total Matches",total_matches)
    col4.metric("Total Innings",total_innings)

    col1 ,col2 =st.columns(2)
    df2= cdata[["Player","Runs"]]
    with col1:
        fig1=px.pie(df2,
               names="Player",
               values="Runs")
        st.plotly_chart(fig1,use_container_width=True)

    df3=cdata[["Player","Runs","Matches","100","6s"]]
    df4=["Runs","Matches","100","6s"]
    select = st.selectbox("Select box",df4)

    fig2 = px.bar(df3,x="Player",y=select)
    with col2:
        st.plotly_chart(fig2,use_container_width=True)


#-------------- Player Comparision------------------#
elif select=="Comparison":
    st.title="Player Comparision"

    players = st.multiselect(
        "Compare Pagal",
        df["Player"],
        default=df["Player"].head(2)
    )

    compare = df[df["Player"].isin(players)]

    fig=px.scatter(
        compare,
        x="Strike_rate",
        y="Ave",
        size="Runs",
        color="Country",
        hover_name="Player"
    )
    st.plotly_chart(fig,use_container_width=True)

#------------------------- Data Explorer-------------------

elif select=="Data Explorer":
    st.title="Data Exploration"

    player1 = st.selectbox("Select Player",df["Player"])

    pldata = df[df["Player"]==player1]

    st.dataframe(pldata)
 