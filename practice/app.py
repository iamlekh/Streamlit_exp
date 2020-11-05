import pandas as pd
import streamlit as st
import plotly.express as px
import numpy as np
import pydeck as pdk


import time
my_bar = st.progress(0)
for percent_complete in range(100):
    time.sleep(0.01)
    my_bar.progress(percent_complete + 1)


@st.cache
def get_data():
    url = "listings.csv"
    return pd.read_csv(url)
df = get_data()


#heading
st.title("Streamlit practice")
st.markdown("Welcome to this practice session...")
st.header("coder quote")
st.markdown(">Hello, *World!* :sunglasses:")


#display dataframe
st.header("render dataframe")
st.dataframe(df.head())
st.subheader("render dataframe with styling ")
df1 = pd.DataFrame(np.random.randn(10, 20),columns=('col %d' % i for i in range(20)))
st.dataframe(df1.style.highlight_max(axis=0))

#display table
st.subheader("render table")
st.markdown("Following are the top five most expensive properties.")
st.write(df.query("price>=800").sort_values("price", ascending=False).head())

#display JSON
st.header("render JSON")
st.subheader("Which host has the most properties listed?")
listingcounts = df.host_id.value_counts()
top_host_1 = df.query('host_id==@listingcounts.index[0]')
top_host_2 = df.query('host_id==@listingcounts.index[1]')
st.write(f"""**{top_host_1.iloc[0].host_name}** is at the top with {listingcounts.iloc[0]} property listings.
**{top_host_2.iloc[1].host_name}** is second with {listingcounts.iloc[1]} listings. Following are randomly chosen
listings from the two displayed as JSON using [`st.json`](https://streamlit.io/docs/api.html#streamlit.json).""")

st.json({top_host_1.iloc[0].host_name: top_host_1\
    [["name", "neighbourhood", "room_type", "minimum_nights", "price"]]\
        .sample(2, random_state=4).to_dict(orient="records"),
        top_host_2.iloc[0].host_name: top_host_2\
    [["name", "neighbourhood", "room_type", "minimum_nights", "price"]]\
        .sample(2, random_state=4).to_dict(orient="records")})

#diaplay linechart
st.write("line chart")
st.line_chart(df['price'].head(100))
#display area chart
st.write("area chart")
st.area_chart(df[['price','number_of_reviews']].head(100))
#display bar chart
st.write("bar chart")
st.bar_chart(df[['price','number_of_reviews']].head(100))

# display pydeck_chart

# st.subheader("pydeck chart")

# st.pydeck_chart(pdk.Deck(
#     map_style='mapbox://styles/mapbox/light-v9',
#     initial_view_state=pdk.ViewState(
#         latitude=37.76,
#         longitude=-122.4,
#         zoom=11,
#         pitch=50,
#     ),
#     layers=[
#         pdk.Layer(
#            'HexagonLayer',
#            data=df,
#            get_position='[latitude, longitude]',
#            radius=200,
#            elevation_scale=4,
#            elevation_range=[0, 1000],
#            pickable=True,
#            extruded=True,
#         ),
#         pdk.Layer(
#             'ScatterplotLayer',
#             data=df,
#             get_position='[latitude, longitude]',
#             get_color='[200, 30, 0, 160]',
#             get_radius=200,
#         ),
#     ],
# ))

#display graphviz_chart
st.subheader("graphviz_chart")
st.graphviz_chart('''
    digraph {
        run -> intr
        intr -> runbl
        runbl -> run
        run -> kernel
        kernel -> zombie
        kernel -> sleep
        kernel -> runmem
        sleep -> swap
        swap -> runswap
        runswap -> new
        runswap -> runmem
        new -> runmem
        sleep -> runmem
    }
''')
#display map
#st.header("Where are the most expensive properties located?")
st.subheader("On a map")
st.markdown("The following map shows the top 1% most expensive Airbnbs priced at $800 and above.")
st.map(df.query("price>=800")[["latitude", "longitude"]].dropna(how="any"))

#display image
st.header("Media")
st.subheader("Images")
pics = {
    "Bike": "https://bd.gaadicdn.com/processedimages/ducati/panigale-v4/source/m_panigale-v4_11540295407.jpg?tr=w-360",
    "Car": "https://wallpapercave.com/wp/wc1754678.jpg"
}
pic = st.selectbox("Picture choices", list(pics.keys()), 0)
st.image(pics[pic], use_column_width=True, caption=pic)


st.subheader("Audio")
audio_file = open('/home/darpan/Documents/Streamlitapp/download.ogg', 'rb')
audio_bytes = audio_file.read()
st.audio(audio_bytes, format='audio/ogg')

# video_file = open('https://www.youtube.com/watch?v=YG15m2VwSjA&list=PLZHQObOWTQDMsr9K-rj53DwVRMYO3t5Yr&index=4')
# video_bytes = video_file.read()

# st.video(video_bytes)


if st.button('Say hello'):
    st.write('Why hello there')
else:
    st.write('Goodbye')

st.balloons()
st.error('Error message')
st.warning('Warning message')
st.info('Info message')
st.success('Success message')



#code
st.header("render code")
st.code("""
@st.cache
def get_data():
    url = "http://data.insideairbnb.com/[...]"
    return pd.read_csv(url)
""", language="python")






st.subheader("Selecting a subset of columns")
st.write(f"Out of the {df.shape[1]} columns, you might want to view only a subset. Streamlit has a [multiselect](https://streamlit.io/docs/api.html#streamlit.multiselect) widget for this.")
defaultcols = ["name", "host_name", "neighbourhood", "room_type", "price"]
cols = st.multiselect("Columns", df.columns.tolist(), default=defaultcols)
st.dataframe(df[cols].head(10))

st.header("Average price by room type")
st.write("You can also display static tables. As opposed to a data frame, with a static table you cannot sorting by clicking a column header.")
st.table(df.groupby("room_type").price.mean().reset_index()\
    .round(2).sort_values("price", ascending=False))
    # .assign(avg_price=lambda x: x.pop("price").apply(lambda y: "%.2f" % y)))





st.header("What is the distribution of property price?")
st.write("""Select a custom price range from the side bar to update the histogram below displayed as a Plotly chart using
[`st.plotly_chart`](https://streamlit.io/docs/api.html#streamlit.plotly_chart).""")
values = st.slider("Price range", float(df.price.min()), float(df.price.clip(upper=1000.).max()), (50., 300.))
# values = st.sidebar.slider("Price range", float(df.price.min()), float(df.price.clip(upper=1000.).max()), (50., 300.))
f = px.histogram(df.query(f"price.between{values}"), x="price", nbins=15, title="Price distribution")
f.update_xaxes(title="Price")
f.update_yaxes(title="No. of listings")
st.plotly_chart(f)


st.header("What is the distribution of availability in various neighborhoods?")
st.write("Using a radio button restricts selection to only one option at a time.")
st.write("💡 Notice how we use a static table below instead of a data frame. \
Unlike a data frame, if content overflows out of the section margin, \
a static table does not automatically hide it inside a scrollable area. \
Instead, the overflowing content remains visible.")
neighborhood = st.radio("Neighborhood", df.neighbourhood_group.unique())
show_exp = st.checkbox("Include expensive listings")
show_exp = " and price<200" if not show_exp else ""


@st.cache
def get_availability(show_exp, neighborhood):
    return df.query(f"""neighbourhood_group==@neighborhood{show_exp}\
        and availability_365>0""").availability_365.describe(\
            percentiles=[.1, .25, .5, .75, .9, .99]).to_frame().T

st.table(get_availability(show_exp, neighborhood))
st.write("At 169 days, Brooklyn has the lowest average availability. At 226, Staten Island has the highest average availability.\
    If we include expensive listings (price>=$200), the numbers are 171 and 230 respectively.")
st.markdown("_**Note:** There are 18431 records with `availability_365` 0 (zero), which I've ignored._")

df.query("availability_365>0").groupby("neighbourhood_group")\
    .availability_365.mean().plot.bar(rot=0).set(title="Average availability by neighborhood group",
        xlabel="Neighborhood group", ylabel="Avg. availability (in no. of days)")
st.pyplot()


st.header("Properties by number of reviews")
st.write("Enter a range of numbers in the sidebar to view properties whose review count falls in that range.")
minimum = st.number_input("Minimum", min_value=0, value=5)
maximum = st.number_input("Maximum", min_value=0, value=5)
# minimum = st.sidebar.number_input("Minimum", min_value=0, value=5)
# maximum = st.sidebar.number_input("Maximum", min_value=0, value=5)
if minimum > maximum:
    st.error("Please enter a valid range")
else:
    df.query("@minimum<=number_of_reviews<=@maximum").sort_values("number_of_reviews", ascending=False)\
        .head(50)[["name", "number_of_reviews", "neighbourhood", "host_name", "room_type", "price"]]



st.write("486 is the highest number of reviews and two properties have it. Both are in the East Elmhurst \
    neighborhood and are private rooms with prices $65 and $45. \
    In general, listings with >400 reviews are priced below $100. \
    A few are between $100 and $200, and only one is priced above $200.")




st.markdown("## Party time!")
st.write("Yay! You're done with this tutorial of Streamlit. Click below to celebrate.")
btn = st.button("Celebrate!")
if btn:
    st.balloons()
