
from matplotlib import pyplot as plt
import streamlit as st
import pandas as pd
import altair as alt
import plotly.express as px
#Model requirements
import numpy as np
from datetime import date, datetime
import plotly.graph_objs as go
from bokeh.plotting import figure


## Time 
now = datetime.now()


# DB Management
import sqlite3 
conn = sqlite3.connect('data.db',check_same_thread = False)
c = conn.cursor()


# Cars table -- Station detection

def view_all_cars(date):
	c.execute('SELECT * FROM carstable WHERE date=?',(date,))
	data = c.fetchall()
	return data

def show_vehicules():
    c.execute('SELECT * FROM vehicules')
    data = c.fetchall()
    return data

def average_time():
    c.execute('SELECT AVG(temps) FROM vehicules')
    data = c.fetchall()
    return data

def weekdays():
    c.execute('SELECT day_name, COUNT(*) AS cars FROM carstable GROUP BY day_name')
    data =c.fetchall()
    return data
# Persons table -- Shop detection

def view_all_persons():
	c.execute('SELECT * FROM shoptable')
	data = c.fetchall()
	return data

## Dashboard -- Data Visualisation

def show_station():

    vehicule= show_vehicules()
    week=weekdays()
    #print avg time

    avt=average_time()[0][0]
    colum1, colum2, colum3 = st.columns(3)

    colum1.metric(label="Temps Moyen", value=int(avt), delta="2 min")
    colum2.metric(label="Total Voitures /Sem", value=7, delta="- 2")
    colum3.metric(label="Utilisation Diesel", value=5, delta=" 3")

    st.text("")
    st.text("")
    ### time
    st.write('Précisez la date que vous voulez visualiser :')
    start_date = st.slider("Quel jour?",value=date(2021, 9, 10),format="DD-MM-YYYY")
    start=start_date.strftime('%Y-%m-%d')
    col1, col2 = st.columns(2)
    with col1:
        
        #### histogramme
        st.write('Nombre de véhicules passés par Heure :')
        st.text("")
        st.text("")
        st.text("")
        station = view_all_cars(start)
        datac = pd.DataFrame(station,columns=["id","type","licence","date","time","day_name"])
        datac['time'] = pd.to_datetime(datac['time'])
        hist_values = np.histogram(datac['time'].dt.hour, bins=24, range=(0,24))[0]
        st.bar_chart(hist_values)

        # chart carburant
        st.text("")
        st.write('Utilisation de Carburant :')
        datav = pd.DataFrame(vehicule,columns=["id","type","licence","temps","Carburant"])
        carb = datav['Carburant'].value_counts().to_frame()
        p1 = px.pie(carb,names=carb.index, values='Carburant')
        st.plotly_chart(p1,use_container_width=True)

    with col2:

        # vehicules type
        st.write('Types de véhicules :')
        datav = pd.DataFrame(vehicule,columns=["id","type","licence","temps","Carburant"])
        vehicules_df = datav['type'].value_counts().to_frame()
        pv = px.pie(vehicules_df,names=vehicules_df.index, values='type')
        st.plotly_chart(pv,use_container_width=True)


        # Week Days
        st.text("")
        df = pd.DataFrame({
        'Day': ["Lundi","Dimanche","Samedi","Vendredi","Jeudi"],
        'Truck': [1,4,3,1,2],
        'Cars': [3,1,5,4,3]},
        columns=['Day', 'Cars', 'Truck'])
        
        df = df.melt('Day', var_name='type', value_name='number')
        
        chart = alt.Chart(df).mark_line().encode( x=alt.X('Day:N'), y=alt.Y('number:Q'), color=alt.Color("type:N")).properties(title="Distribution Par Jour de Semaine")
        st.altair_chart(chart, use_container_width=True)

    

    with st.expander("Liste des véhicules détecté"):
        datav = pd.DataFrame(vehicule,columns=["id","type","licence","temps","Carburant"])
        st.table(datav[['type','licence']])


def show_shop():

    shop = view_all_persons()

    colum1, colum2, colum3 = st.columns(3)
    colum1.metric(label="Total Visiteurs'", value=18, delta="5 ")
    colum2.metric(label="Male", value=10, delta="- 2")
    colum3.metric(label="Female", value=8, delta=" 3")
    

    col1, col2 = st.columns(2)
    with col1:

        st.text("")
        st.text("")
        st.text("")
        st.write('Visiteurs du Shop :')
        
        datag = pd.DataFrame(shop,columns=["id","gender","date","time"])
        datag['time'] = pd.to_datetime(datag['time'])
        hist_values = np.histogram(datag['time'].dt.hour, bins=24, range=(0,24))[0]
        st.bar_chart(hist_values)
        st.text("")
        st.text("")
        st.text("")

        st.write('Distribution des visiteurs :')
        datap = pd.DataFrame(shop,columns=["id","gender","date","time"])
        person_df = datap['gender'].value_counts().to_frame()
        #st.dataframe(person_df)
        #person_df = person_df.reset_index()
        p1 = px.pie(person_df,names=person_df.index, values='gender')
        st.plotly_chart(p1,use_container_width=True)

    with col2:

        st.write('Selon les tranches d age :')

        labels = '<25', '25-35', '45-55', '>55'
        sizes = [3, 7, 5, 3]
        explode = (0, 0.1, 0, 0)  
        
        fig1, ax1 = plt.subplots()
        ax1.pie(sizes, explode=explode, labels=labels, autopct='%1.1f%%',shadow=True, startangle=90)
        ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
        st.pyplot(fig1)


        st.write('Selon le Jours de la Semaine :')
        st.text("")
        st.text("")
        st.text("")
        df = pd.DataFrame({
        'Jour': ["Dimanche","Lundi","Samedi","Vendredi","Jeudi"],
        'Hommes': [2,1,3,1,2],
        'Femmes': [1,3,2,4,2]},
        columns=['Jour', 'Hommes', 'Femmes'])
        
        df = df.melt('Jour', var_name='Genre', value_name='number')
        
        chart = alt.Chart(df).mark_line().encode( x=alt.X('Jour:N'), y=alt.Y('number:Q'), color=alt.Color("Genre:N")).properties(title="Distribution Par Jour de Semaine")
        st.altair_chart(chart, use_container_width=True)

        
        


    with st.expander("Table des visiteurs"):
        datagen = pd.DataFrame(shop,columns=["id","gender","date","time"])
        st.table(datagen[['gender','date','time']])
    

    
    

    


    
