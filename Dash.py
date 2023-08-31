import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import requests
import seaborn as sns
import numpy as np
import requests 
from PIL import Image
import streamlit as st
from streamlit_lottie import st_lottie
from streamlit_option_menu import option_menu
import wikipediaapi
import wikipedia


st.set_page_config(page_title="IPL 2022 Dashboard", page_icon=":mortar_board:", layout="wide",initial_sidebar_state="expanded")

#dataset 
df = pd.read_csv('IPL_Matches_2022.csv')

# Use for lottie animation

def load_lottieurl(url):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

# Use Local CSS File
def css(file_name):
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

css("style/style.css")
css("style/hide_menu.css")


#Assets

lottie_url = "https://assets1.lottiefiles.com/packages/lf20_p4q9ra7d.json"
lottie_anime = load_lottieurl(lottie_url)

lottie_url = "https://assets7.lottiefiles.com/private_files/lf30_gpi1jcpe.json"
lottie_conclusion = load_lottieurl(lottie_url)

#Team logo 
img1 = Image.open("logo/GT.png")
img2 = Image.open("logo/LSG.png")
img3 = Image.open("logo/RR.png")
img4 = Image.open("logo/RCB.png")
img5 = Image.open("logo/DC.png")
img6 = Image.open("logo/KKR.png")
img7 = Image.open("logo/PBKS.png")
img8 = Image.open("logo/SRH.png")
img9 = Image.open("logo/CSK.png")
img10 = Image.open("logo/MI.png")
img11 = Image.open("logo/IPL.png")

#creating sidebar menu

with st.sidebar:
    selected = option_menu(
                menu_title=None,  # required
                options=["Home", "Gujarat Titans", "Lucknow Super Giants", "Rajasthan Royals", "Royal Challenger Bangalore","Delhi Capitals", "Kolkata Knight Riders","Punjab Kings", "Sunrisers Hyderabad","Chennai Super Kings", "Mumbai Indians"],  # required
                icons=["house", "book", "book","book", "book","book", "book","book", "book","book", "book",],  # optional0
                menu_icon="cast",  # optional
                default_index=0,  # optional
    )

if selected == "Home":
    with st.container():
                
        st.title("IPL Analysis Dashboard 2022")
        st_lottie(lottie_anime,height=300)
            
                
        
    with st.container():
            st.write('---')
            left_column,right_column=st.columns(2)
            with left_column:
                st.header("Welcome !")
                st.write("""

                -   In this analysis, I used the IPL_Matches_2022.csv file from the kaggle Dataset
                -   This is a Dashboard for 59 group stage matches
                -   In this data Analysis,We will be using various Libraries such as pandas, Numpy, Seaborn & Matplotlib""")
            with right_column:
                st.image(img11,width=160)
    with st.container():
            st.write('---')
            
            left_column,right_column = st.columns(2)

            with left_column:
                st.subheader("Questions on dataset ipl 2022")

                st.write("##")
                st.write("""
                -   What was the most preferred Decision On winning Toss i.e. Choose To Bat / Choose To Field
                -   Which team wins the maximum number of matches in this season
                -   Which Venue has hosted the Most Number Of Ipl Matches
                -   Who has been awarded with Player Of the Max maximum Number Of Times""")

            with right_column:
                st_lottie(lottie_conclusion,height=300)
    with st.container():
        st.write('---')

        st.header("Lets check team ranking")
        df = pd.read_csv('IPL_Matches_2022.csv')
        Winner_df = df.groupby('WinningTeam')[['ID']].count()
        Winner_df = Winner_df.sort_values('ID', ascending=False).reset_index()
        Winner_df.rename(columns = {'ID':'Wins','WinningTeam':'Teams'},inplace=True)
        Winner_df
        #Plotting Wins vs Teams
        #We will be assigning colour code to teams to make it easily understandable
        fig = px.bar(
                Winner_df,
                x='Teams',
                y='Wins',
                color = 'Teams',
                color_continuous_scale = ['blue','teal','pink','green','navy','magenta','red','orange','yellow','cyan'],
                template='plotly_white',
                title='<b>Matches Won By Each Team</b>'
            )
        st.plotly_chart(fig)
        st.write("""
            - Seems Gujarat Titans Have won the Most matches in IPL 2022 Till Date. Followed by Lucknow Super Giants
            """)

        st.write("---")
        #Q1. What was the most preferred Decision On winning Toss i.e. Bat / Field 
        # We can see toss decision is either bat/field
        st.header("Lets check most preferred decision")
        df.TossDecision.unique()
        decision_df = df.groupby('TossDecision')[['ID']].count()
        decision_df = decision_df.sort_values('ID').reset_index()
        decision_df.rename(columns={'ID':'Total','TossDecision':'Decision'},inplace=True)
        decision_df
        #Lets plot the Result
        fig1 = px.bar(
                decision_df,
                x='Decision',
                y='Total',
                color = 'Decision',
                color_continuous_scale = ['#4863A0','#566D7E'],
                template='plotly_white',
                title='<b>Preferred Decision</b>'
            )
        st.plotly_chart(fig1)
        
        #Q2. Which Decision has proved most beneficial i.e Field / Bat
        field_df = df.loc[(df['TossWinner'] == df['WinningTeam']) & (df['TossDecision'] == 'field'), ['ID', 'WinningTeam','TossDecision']]
        field_df.WinningTeam.count()
        bat_df = df.loc[(df['TossWinner'] == df['WinningTeam']) & (df['TossDecision'] == 'bat'), ['ID', 'WinningTeam','TossDecision']]
        bat_df.WinningTeam.count()
        frames = [bat_df, field_df]
        result_df = pd.concat(frames)
        result_df = result_df.groupby('TossDecision')[['ID']].count()

        st.write("""
        - After Analysis we know that,52 times toss winning Team Choose to Field First and only 7 Times batting was choosen""")

        
        # Now Lets Plot the New Understanding Regarding the Success of these decisions
        result_df = result_df.sort_values('ID').reset_index()
        result_df.rename(columns={'ID':'Total','TossDecision':'Decision'},inplace=True)
        result_df

        fig2=plt.figure()
        plt.title('<b>Decision Success</b>')
        plt.xlabel('<b>Decision</b>')
        plt.ylabel('<b>Total</b>')
        plt.tick_params()
        plt.bar(decision_df.Decision, decision_df.Total, color=['#4CC552','#4CC552'])
        plt.bar(result_df.Decision, result_df.Total, color=['#00FF00','#00FF00'])
        plt.legend(['Decision Taken','Decision Proved Right'])
        st.plotly_chart(fig2)

        st.write("""
        - As from Analysis we know that ,26 times fielding decision  and  4 Times batting decision was successful""")

        st.header("Lets see how many venues have hosted the Ipl Matches")
        venue_df = df.groupby('Venue')[['ID']].count()
        venue_df = venue_df.sort_values('ID',ascending=False).reset_index()
        venue_df.rename(columns={'ID':'Total_Match','Venue':'Stadium'},inplace=True)
        labels = list(venue_df.Stadium)
        venue_df
        
        fig3 = px.bar(
                venue_df,
                x='Stadium',
                y='Total_Match',
                color = 'Stadium',
                color_continuous_scale = ['green','magenta','red','yellow'],
                template='plotly_white',
                title='<b>Total Matches played in stadium</b>'
            )
        st.plotly_chart(fig3)

        pi=plt.figure()
        plt.title("<b>Venues</b>")
        sizes=venue_df.Total_Match
        explode=(0.1,0,0,0)
        pi, ax1 = plt.subplots()
        ax1.pie(sizes, explode=explode, labels=labels, autopct='%1.1f%%',
        shadow=True, startangle=90)
        st.pyplot(pi)

        st.write("""
        - So We can See the most Number of matches were played at Dr DY Patil Sports Academy Stadium(18) Followed By Wankhede Stadium (16)
        """)

        
        st.header("Lets Check top 10 player who won the man of match award")
        player_df = df.groupby('Player_of_Match')[['ID']].count()
        player_df = player_df.sort_values('ID',ascending=False).reset_index()
        players_df = player_df.head(10).copy()
        players_df.rename(columns={'ID':'Total_Awards','Player_of_Match':'Man_Of_The_Match'},inplace=True)
        labels1 = list(players_df.Man_Of_The_Match)
        players_df

        fig4=plt.figure()
        plt.title("Man_Of_The_Match")
        sizes=players_df.Total_Awards
        explode=(0.1,0,0,0,0,0,0,0,0,0)
        fig4, ax1 = plt.subplots()
        ax1.pie(sizes, explode=explode, labels=labels1, autopct='%1.1f%%',
        shadow=False, startangle=90)
        st.pyplot(fig4)

    with st.container():
        st.write("---")
        st.header("Conclusion")

        st.subheader("Following are my conclusions about this datset")
        st.write("##")
        st.write("""
        -   A total of 59 matches have been played
        -   Most number of Matches were played in Dr DY Patil Sports Academy, Mumbai[18]
        -   Most preferable choice after winning toss is to field first
        -   52 times fielding and 7 times batting is choosed by Toss Winner
        -   Gujarat Titans Have Won the Most Number of Matches (9) followed by Lukhnow Super Gaints with (8) Matches
        -   Dr DY Patil Sports Academy (Stadium) Hosted the Most Number of Matches (18) followed by wankhede Stadium (16)
        -   Kuldeep Yadav has been the Man Of The Match Most Number of Times with 4 Awards""")
        
        st.write("---")
        st.header(":mailbox: For feedback !")


    contact_form = """
    <form action="https://formsubmit.co/rana.rahul0424@gmail.com" method="POST">
        <input type="hidden" name="_captcha" value="false">
        <input type="text" name="name" placeholder="Your name" required>
        <input type="email" name="email" placeholder="Your email" required>
        <textarea name="message" placeholder="Your message here"></textarea>
        <button type="submit">Send</button>
    </form>
    """

    st.markdown(contact_form, unsafe_allow_html=True)
   
if selected ==  "Gujarat Titans":
    left_column,right_column = st.columns(2)
    with left_column:
        st.title(f"{selected}")
        
        
    with right_column:
        st.image(img1,width=200)

    
    st.write("---")
    #search using wikipedia module
    link = wikipedia.search(f"{selected}")
    #data extraction using wikipedia-api module
    wiki_wiki=wikipediaapi.Wikipedia(language='en',
    extract_format=wikipediaapi.ExtractFormat.WIKI)
    st.write(wiki_wiki.page(f"{selected}").text)
    st.write(wikipedia.page(f"{selected}").url)


if selected == "Lucknow Super Giants":
    left_column,right_column = st.columns(2)
    with left_column:
        st.title(f"{selected}")
        
    with right_column:
        st.image(img2,width=250)

    st.write("---")
    #search using wikipedia module
    link = wikipedia.search(f"{selected}")
    #data extraction using wikipedia-api module
    wiki_wiki=wikipediaapi.Wikipedia(language='en',
    extract_format=wikipediaapi.ExtractFormat.WIKI)
    st.write(wiki_wiki.page(f"{selected}").text)
    st.write(wikipedia.page(f"{selected}").url)

if selected ==  "Rajasthan Royals":
    left_column,right_column = st.columns(2)
    with left_column:
        st.title(f"{selected}")

        
    with right_column:
        st.image(img3,width=200)

    st.write("---")
    #search using wikipedia module
    link = wikipedia.search(f"{selected}")
    #data extraction using wikipedia-api module
    wiki_wiki=wikipediaapi.Wikipedia(language='en',
    extract_format=wikipediaapi.ExtractFormat.WIKI)
    st.write(wiki_wiki.page(f"{selected}").text)
    st.write(wikipedia.page(f"{selected}").url)

if selected == "Royal Challenger Bangalore":
    left_column,right_column = st.columns(2)
    with left_column:
        st.title(f"{selected}")
        
    with right_column:
        st.image(img4,width=200)

    st.write("---")
    #search using wikipedia module
    link = wikipedia.search(f"{selected}")
    #data extraction using wikipedia-api module
    wiki_wiki=wikipediaapi.Wikipedia(language='en',
    extract_format=wikipediaapi.ExtractFormat.WIKI)
    st.write(wiki_wiki.page(f"{selected}").text)
    st.write(wikipedia.page(f"{selected}").url)

if selected ==  "Delhi Capitals":
    left_column,right_column = st.columns(2)
    with left_column:
        st.title(f"{selected}")

        
    with right_column:
        st.image(img5,width=200)

    st.write("---")
    #search using wikipedia module
    link = wikipedia.search(f"{selected}")
    #data extraction using wikipedia-api module
    wiki_wiki=wikipediaapi.Wikipedia(language='en',
    extract_format=wikipediaapi.ExtractFormat.WIKI)
    st.write(wiki_wiki.page(f"{selected}").text)
    st.write(wikipedia.page(f"{selected}").url)

if selected == "Kolkata Knight Riders":
    left_column,right_column = st.columns(2)
    with left_column:
        st.title(f"{selected}")
        
    with right_column:
        st.image(img6,width=150)

    st.write("---")
    #search using wikipedia module
    link = wikipedia.search(f"{selected}")
    #data extraction using wikipedia-api module
    wiki_wiki=wikipediaapi.Wikipedia(language='en',
    extract_format=wikipediaapi.ExtractFormat.WIKI)
    st.write(wiki_wiki.page(f"{selected}").text)
    st.write(wikipedia.page(f"{selected}").url)

if selected ==  "Punjab Kings":
    left_column,right_column = st.columns(2)
    with left_column:
        st.title(f"{selected}")
        
    with right_column:
        st.image(img7,width=150)

    st.write("---")
    #search using wikipedia module
    link = wikipedia.search(f"{selected}")
    #data extraction using wikipedia-api module
    wiki_wiki=wikipediaapi.Wikipedia(language='en',
    extract_format=wikipediaapi.ExtractFormat.WIKI)
    st.write(wiki_wiki.page(f"{selected}").text)
    st.write(wikipedia.page(f"{selected}").url)

if selected == "Sunrisers Hyderabad":
    left_column,right_column = st.columns(2)
    with left_column:
        st.title(f"{selected}")
        
    with right_column:
        st.image(img8,width=250)

    st.write("---")
    #search using wikipedia module
    link = wikipedia.search(f"{selected}")
    #data extraction using wikipedia-api module
    wiki_wiki=wikipediaapi.Wikipedia(language='en',
    extract_format=wikipediaapi.ExtractFormat.WIKI)
    st.write(wiki_wiki.page(f"{selected}").text)
    st.write(wikipedia.page(f"{selected}").url)

if selected ==  "Chennai Super Kings":
    left_column,right_column = st.columns(2)
    with left_column:
        st.title(f"{selected}")
        
        
    with right_column:
        st.image(img9,width=200)

    st.write("---")
    #search using wikipedia module
    link = wikipedia.search(f"{selected}")
    #data extraction using wikipedia-api module
    wiki_wiki=wikipediaapi.Wikipedia(language='en',
    extract_format=wikipediaapi.ExtractFormat.WIKI)
    st.write(wiki_wiki.page(f"{selected}").text)
    st.write(wikipedia.page(f"{selected}").url)

if selected == "Mumbai Indians":
    left_column,right_column = st.columns(2)
    with left_column:
        st.title(f"{selected}")

        
    with right_column:
        st.image(img10,width=250)

    st.write("---")
    #search using wikipedia module
    link = wikipedia.search(f"{selected}")
    #data extraction using wikipedia-api module
    wiki_wiki=wikipediaapi.Wikipedia(language='en',
    extract_format=wikipediaapi.ExtractFormat.WIKI)
    st.write(wiki_wiki.page(f"{selected}").text)
    st.write(wikipedia.page(f"{selected}").url)
