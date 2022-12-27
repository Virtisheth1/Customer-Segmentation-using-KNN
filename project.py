import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

# --- Initialising SessionState ---
if "load_state" not in st.session_state:
     st.session_state.load_state = False
     st.session_state.drop_state = False
     st.session_state.train_state = False
     st.session_state.display_state = False          
     st.session_state.radio_state = False 
     st.session_state.categorical_convert = False    
     st.session_state.cluster_name = {}


uploaded_file = st.file_uploader("Choose a file")

if uploaded_file is not None:

  df = pd.read_csv(uploaded_file)
  df2 = df
  df = df
  st.write(df)
      
  st.session_state.load_state = True
  drop_options = st.multiselect('What Field do you Want to Drop',list(df.columns),[])

  if(st.button("Drop Columns or Continue") or st.session_state.drop_state):
    st.session_state.drop_state = True
    df = df.drop(drop_options, axis=1)
    st.write(df)

    if object in list(df.dtypes):
      categorical_convert = st.multiselect('Which Categorical Field do you Want to Convert',list(df.columns),[])
      if(st.button("Convert Categorical Data or Continue") or st.session_state.categorical_convert):
        st.session_state.categorical_convert = True
        df = pd.get_dummies(df, columns = categorical_convert)
        st.write(df)

        scaler = StandardScaler()
        X = scaler.fit_transform(df.values)

        clusters = range(3,30)
        inertia = []
        fig = plt.figure() 
        for n in clusters:
            kmeans = KMeans(n_clusters=n)
            kmeans.fit(X) 
            inertia.append(kmeans.inertia_)
        plt.plot(clusters, inertia)
        st.pyplot(fig)

        cluster = int(st.number_input('Enter No. of Clusters'))

        if(st.button("Train Model") or st.session_state.train_state):   ####Train
          st.session_state.train_state = True
          kmeans = KMeans(n_clusters=cluster, random_state=42)
          kmeans.fit(X)
          df2['labels'] = kmeans.predict(X)

          radio = st.radio("Display Cluster by",("By Label","By Name"))

          if radio=='By Label':
            label_no = int(st.number_input('Label No'))
            
          if(st.button("Display Cluster") or st.session_state.display_state ):
            st.session_state.display_state = True
            st.write(df2[df2['labels']==label_no].head(10))
            name = st.text_input("Name the Cluster","")
            if(st.button("Name the Cluster")):
              st.session_state.cluster_name.update({name:label_no})
              
          if radio=='By Name':
            label_name = st.selectbox("Select Cluster",tuple(st.session_state.cluster_name.keys()))
            label_no = st.session_state.cluster_name[label_name]
            df = df2[df2['labels']==label_no]
            st.write(df)
            csv = df.to_csv(index=False).encode('utf-8')
            st.download_button("Press to Download",csv,label_name+".csv","text/csv",key='download-csv')
              








    else:
        scaler = StandardScaler()
        X = scaler.fit_transform(df.values)

        clusters = range(3,30)
        inertia = []
        fig = plt.figure() 
        for n in clusters:
            kmeans = KMeans(n_clusters=n)
            kmeans.fit(X) 
            inertia.append(kmeans.inertia_)
        plt.plot(clusters, inertia)
        st.pyplot(fig)

        cluster = int(st.number_input('Enter No. of Clusters'))

        if(st.button("Train Model") or st.session_state.train_state):   #####Train
          st.session_state.train_state = True
          kmeans = KMeans(n_clusters=cluster, random_state=42)
          kmeans.fit(X)
          df2['labels'] = kmeans.predict(X)

          radio = st.radio("Display Cluster by",("By Label","By Name"))

          if radio=='By Label':
            label_no = int(st.number_input('Label No'))
            
          if(st.button("Display Cluster") or st.session_state.display_state ):
            st.session_state.display_state = True
            st.write(df2[df2['labels']==label_no].head(10))
            name = st.text_input("Name the Cluster","")
            if(st.button("Name the Cluster")):
              st.session_state.cluster_name.update({name:label_no})
              
          if radio=='By Name':
            label_name = st.selectbox("Select Cluster",tuple(st.session_state.cluster_name.keys()))
            label_no = st.session_state.cluster_name[label_name]
            df = df2[df2['labels']==label_no]
            st.write(df)
            csv = df.to_csv(index=False).encode('utf-8')
            st.download_button("Press to Download",csv,label_name+".csv","text/csv",key='download-csv')
          