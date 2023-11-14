from emoji import emoji_count
from soupsieve import select
import streamlit as st;
import preprocess ;
import re;
import stats;
import matplotlib.pyplot as plt;
import seaborn as sns;
import numpy as np;

st.sidebar.title("Whatsapp Chat Analyzer")

uploaded_file=st.sidebar.file_uploader("Choose a file")

if uploaded_file is not None:
    bytes_data=uploaded_file.getvalue()
    
    data=bytes_data.decode('utf-8')
    
    df=preprocess.preprocess(data)
    
    st.dataframe(df)
    
    user_list=df['User'].unique().tolist()
    
    user_list.remove('Group Notification')
    
    user_list.sort()
    
    user_list.insert(0,'Overall')
    
    selected_user=st.sidebar.selectbox("Show Analysis with respect to",user_list)
    
    st.title(f"Whatsapp Chat Analysis for {selected_user}")
    
    if st.sidebar.button("Show Analysis"):
        num_messages,num_words,media_omitted,links=stats.fetchstats(selected_user,df)
        
        col1,col2,col3,col4=st.columns(4)
        
        with col1:
            st.header('Total Messages')
            st.title(num_messages)
            
        with col2:
            st.header('Total No of Words')
            st.title(num_words)
        
        with col3:
            
            st.header('Total Media Shared')
            st.title(media_omitted)
        
        with col4:
            st.header('Total Links Shared')
            st.title(links)
            
        if selected_user=='Overall':
            st.title('Most Busy Users')
            
            busycount,newdf=stats.fetchbusyuser(df)
            fig,ax=plt.subplots()
            col1,col2=st.columns(2)
            
            with col1:
                sns.barplot(x=busycount.index,y=busycount.values,data=newdf,palette='plasma')
                plt.xticks(rotation='vertical')
                st.pyplot(fig)
                
            with col2:
                st.dataframe(newdf)
                
                
        st.title('Word Cloud')
        df_img=stats.createwordcloud(selected_user,df)
        fig,ax=plt.subplots()
        plt.axis(False)
        ax.imshow(df_img)
        st.pyplot(fig)
        
        most_common_df=stats.getcommonwords(selected_user,df)
        fig,ax=plt.subplots()
        sns.barplot(x=most_common_df[1],y=most_common_df[0])
        st.title('Most Common Words')
        st.pyplot(fig)
        
        emoji_df=stats.getemojistats(selected_user,df)
        emoji_df.columns=['Emoji','Count']
        st.title('Emoji Analysis')
        
        col1,col2=st.columns(2)
        with col1:
            st.dataframe(emoji_df)
            
        with col2:
            emojicount=list(emoji_df['Count'])
            perlist=[(i/sum(emojicount))*100 for i in emojicount]
            emoji_df['Percentage use']=np.array(perlist)
            st.dataframe(emoji_df)   
            
        st.title('Monthly Timeline')
        
        time=stats.monthtimeline(selected_user,df)
        fig,ax=plt.subplots()
        ax.plot(time['Time'],time['Messages'],color='#E0144C')
        plt.xticks(rotation='vertical')
        plt.tight_layout()
        st.pyplot(fig)
        
        st.title("Activity Maps")
        
        col1,col2=st.columns(2)
        
        with col1:
            st.header('Most Busy Day')
            
            busy_day=stats.weekactivitymap(selected_user,df)
            fig,ax=plt.subplots()
            sns.barplot(x=busy_day.index,y=busy_day.values)
            plt.xticks(rotation='vertical')
            plt.tight_layout()
            st.pyplot(fig)
            
        with col2:
            st.header('Most Busy Month')
            busy_month=stats.monthactivitymap(selected_user,df)
            fig,ax=plt.subplots()
            sns.barplot(x=busy_month.index,y=busy_month.values)
            plt.xticks(rotation='vertical')
            plt.tight_layout()
            st.pyplot(fig)
    
      
        
                    
                