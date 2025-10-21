# %% [markdown]
# <img src="https://upload.wikimedia.org/wikipedia/commons/thumb/5/58/Uber_logo_2018.svg/1024px-Uber_logo_2018.svg.png" alt="UBER LOGO" width="50%" />
#
# # UBER Pickups

# %% [markdown]
# ## Company's Description 📇
#
# <a href="http://uber.com/" target="_blank">Uber</a> is one of the most famous startup in the world. It started as a ride-sharing application for people who couldn't afford a taxi. Now, Uber expanded its activities to Food Delivery with <a href="https://www.ubereats.com/fr-en" target="_blank">Uber Eats</a>, package delivery, freight transportation and even urban transportation with <a href="https://www.uber.com/fr/en/ride/uber-bike/" target="_blank"> Jump Bike</a> and <a href="https://www.li.me/" target="_blank"> Lime </a> that the company funded.
#
#
# The company's goal is to revolutionize transportation accross the globe. It operates now on about 70 countries and 900 cities and generates over $14 billion revenue! 😮
#

# %% [markdown]
# ## Project 🚧
#
# One of the main pain point that Uber's team found is that sometimes drivers are not around when users need them. For example, a user might be in San Francisco's Financial District whereas Uber drivers are looking for customers in Castro.
#
# (If you are not familiar with the bay area, check out <a href="https://www.google.com/maps/place/San+Francisco,+CA,+USA/@37.7515389,-122.4567213,13.43z/data=!4m5!3m4!1s0x80859a6d00690021:0x4a501367f076adff!8m2!3d37.7749295!4d-122.4194155" target="_blank">Google Maps</a>)
#
# Eventhough both neighborhood are not that far away, users would still have to wait 10 to 15 minutes before being picked-up, which is too long. Uber's research shows that users accept to wait 5-7 minutes, otherwise they would cancel their ride.
#
# Therefore, Uber's data team would like to work on a project where **their app would recommend hot-zones in major cities to be in at any given time of day.**

# %% [markdown]
# ## Goals 🎯
#
# Uber already has data about pickups in major cities. Your objective is to create algorithms that will determine where are the hot-zones that drivers should be in. Therefore you will:
#
# * Create an algorithm to find hot zones
# * Visualize results on a nice dashboard

# %% [markdown]
# ## Scope of this project 🖼️
#
# To start off, Uber wants to try this feature in New York city. Therefore you will only focus on this city. Data can be found here:
#
# 👉👉<a href="https://full-stack-bigdata-datasets.s3.eu-west-3.amazonaws.com/Machine+Learning+non+Supervis%C3%A9/Projects/uber-trip-data.zip" target="_blank"> Uber Trip Data</a> 👈👈
#
# **You only need to focus on New York City for this project**

# %% [markdown]
# ## Helpers 🦮
#
# To help you achieve this project, here are a few tips that should help you:
#
# ### Clustering is your friend
#
# Clustering technics are a perfect fit for the job. Think about it, all the pickup locations can be gathered into different clusters. You can then use **cluster coordinates to pin hot zones** 😉
#
#
# ### Create maps with `plotly`
#
# Check out <a href="https://plotly.com/" target="_blank">Plotly</a> documentation, you can create maps and populate them easily. Obviously, there are other libraries but this one should do the job pretty well.
#
#
# ### Start small grow big
#
# Eventhough Uber wants to have hot-zones per hour and per day of week, you should first **start small**. Pick one day at a given hour and **then start to generalize** your approach.

# %% [markdown]
# ## Deliverable 📬
#
# To complete this project, your team should:
#
# * Have a map with hot-zones using any python library (`plotly` or anything else).
# * You should **at least** describe hot-zones per day of week.
# * Compare results with **at least** two unsupervised algorithms like KMeans and DBScan.
#
# Your maps should look something like this:
#
# <img src="https://full-stack-assets.s3.eu-west-3.amazonaws.com/images/Clusters_uber_pickups.png" alt="Uber Cluster Map" />

# %%
def detect_outliers_iqr(data, column):
    Q1 = data[column].quantile(0.25)
    Q3 = data[column].quantile(0.75)
    IQR = Q3 - Q1

    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR

    outliers = data[(data[column] < lower_bound) | (data[column] > upper_bound)]
    return outliers


# Most of this code is from Geoff Boeing article.
# If you get lost, read through it and it will explain way better than I could ever do!
# https://geoffboeing.com/2014/08/clustering-to-reduce-spatial-data-set-size/


def get_hot_spots(max_distance, min_cars, ride_data):
    ## get coordinates from ride data
    coords = ride_data[["Lat", "Lon"]].to_numpy()

    ## calculate epsilon parameter using
    ## the user defined distance
    kms_per_radian = 6371.0088
    ##The epsilon parameter is the max distance that points can be from each other to be considered a cluster.
    epsilon = max_distance / kms_per_radian

    ## perform clustering
    db = DBSCAN(
        eps=epsilon, min_samples=min_cars, algorithm="ball_tree", metric="haversine"
    ).fit(np.radians(coords))

    ## group the clusters
    cluster_labels = db.labels_
    num_clusters = len(set(cluster_labels))
    clusters = pd.Series([coords[cluster_labels == n] for n in range(num_clusters)])

    ## report
    print("Number of clusters: {}".format(num_clusters))

    ## initialize lists for hot spots
    lat = []
    lon = []
    num_members = []

    ## loop through clusters and get centroids, number of members
    for ii in range(len(clusters)):
        ## filter empty clusters
        if clusters[ii].any():
            ## get centroid and magnitude of cluster
            lat.append(MultiPoint(clusters[ii]).centroid.x)
            lon.append(MultiPoint(clusters[ii]).centroid.y)
            num_members.append(len(clusters[ii]))

    hot_spots = [lon, lat, num_members]

    return hot_spots


# %% [markdown]
# # Rendu
# La première chose est d'examiner l'allure textuel des fichiers qui sont volumineux.
# En examinant les fcihiers décompressés du repertoire , nous avons les fichiers suivant avec leur taille.
# * 7,5K 14 jan  2016 taxi-zone-lookup.csv
# *  25M 14 jan  2016 uber-raw-data-apr14.csv
# *  37M 14 jan  2016 uber-raw-data-aug14.csv
# * 526M  8 oct  2015 uber-raw-data-janjune-15.csv
# *  35M 14 jan  2016 uber-raw-data-jul14.csv
# *  29M 14 jan  2016 uber-raw-data-jun14.csv
# *  29M 14 jan  2016 uber-raw-data-may14.csv
# *  45M 14 jan  2016 uber-raw-data-sep14.csv
#
#
# La commande ci-dessous en bash nous permet d'appréhender l'allure des fichiers.
# ```head uber-raw-data-*.csv```
# ```bash
# ==> uber-raw-data-apr14.csv <==
# "Date/Time","Lat","Lon","Base"
# "4/1/2014 0:11:00",40.769,-73.9549,"B02512"
# "4/1/2014 0:17:00",40.7267,-74.0345,"B02512"
# "4/1/2014 0:21:00",40.7316,-73.9873,"B02512"
# "4/1/2014 0:28:00",40.7588,-73.9776,"B02512"
# "4/1/2014 0:33:00",40.7594,-73.9722,"B02512"
# "4/1/2014 0:33:00",40.7383,-74.0403,"B02512"
# "4/1/2014 0:39:00",40.7223,-73.9887,"B02512"
# "4/1/2014 0:45:00",40.762,-73.979,"B02512"
# "4/1/2014 0:55:00",40.7524,-73.996,"B02512"
#
# ==> uber-raw-data-aug14.csv <==
# "Date/Time","Lat","Lon","Base"
# "8/1/2014 0:03:00",40.7366,-73.9906,"B02512"
# "8/1/2014 0:09:00",40.726,-73.9918,"B02512"
# "8/1/2014 0:12:00",40.7209,-74.0507,"B02512"
# "8/1/2014 0:12:00",40.7387,-73.9856,"B02512"
# "8/1/2014 0:12:00",40.7323,-74.0077,"B02512"
# "8/1/2014 0:13:00",40.7349,-74.0033,"B02512"
# "8/1/2014 0:15:00",40.7279,-73.9542,"B02512"
# "8/1/2014 0:17:00",40.721,-73.9937,"B02512"
# "8/1/2014 0:19:00",40.7195,-74.006,"B02512"
#
# ==> uber-raw-data-janjune-15.csv <==
# Dispatching_base_num,Pickup_date,Affiliated_base_num,locationID
# B02617,2015-05-17 09:47:00,B02617,141
# B02617,2015-05-17 09:47:00,B02617,65
# B02617,2015-05-17 09:47:00,B02617,100
# B02617,2015-05-17 09:47:00,B02774,80
# B02617,2015-05-17 09:47:00,B02617,90
# B02617,2015-05-17 09:47:00,B02617,228
# B02617,2015-05-17 09:47:00,B02617,7
# B02617,2015-05-17 09:47:00,B02764,74
# B02617,2015-05-17 09:47:00,B02617,249
#
# ==> uber-raw-data-jul14.csv <==
# "Date/Time","Lat","Lon","Base"
# "7/1/2014 0:03:00",40.7586,-73.9706,"B02512"
# "7/1/2014 0:05:00",40.7605,-73.9994,"B02512"
# "7/1/2014 0:06:00",40.732,-73.9999,"B02512"
# "7/1/2014 0:09:00",40.7635,-73.9793,"B02512"
# "7/1/2014 0:20:00",40.7204,-74.0047,"B02512"
# "7/1/2014 0:35:00",40.7487,-73.9869,"B02512"
# "7/1/2014 0:57:00",40.7444,-73.9961,"B02512"
# "7/1/2014 0:58:00",40.7132,-73.9492,"B02512"
# "7/1/2014 1:04:00",40.759,-73.973,"B02512"
#
# ==> uber-raw-data-jun14.csv <==
# "Date/Time","Lat","Lon","Base"
# "6/1/2014 0:00:00",40.7293,-73.992,"B02512"
# "6/1/2014 0:01:00",40.7131,-74.0097,"B02512"
# "6/1/2014 0:04:00",40.3461,-74.661,"B02512"
# "6/1/2014 0:04:00",40.7555,-73.9833,"B02512"
# "6/1/2014 0:07:00",40.688,-74.1831,"B02512"
# "6/1/2014 0:08:00",40.7152,-73.9917,"B02512"
# "6/1/2014 0:08:00",40.7282,-73.991,"B02512"
# "6/1/2014 0:08:00",40.3042,-73.9794,"B02512"
# "6/1/2014 0:09:00",40.727,-73.9915,"B02512"
#
# ==> uber-raw-data-may14.csv <==
# "Date/Time","Lat","Lon","Base"
# "5/1/2014 0:02:00",40.7521,-73.9914,"B02512"
# "5/1/2014 0:06:00",40.6965,-73.9715,"B02512"
# "5/1/2014 0:15:00",40.7464,-73.9838,"B02512"
# "5/1/2014 0:17:00",40.7463,-74.0011,"B02512"
# "5/1/2014 0:17:00",40.7594,-73.9734,"B02512"
# "5/1/2014 0:20:00",40.7685,-73.8625,"B02512"
# "5/1/2014 0:21:00",40.7637,-73.9962,"B02512"
# "5/1/2014 0:21:00",40.7252,-74.0023,"B02512"
# "5/1/2014 0:25:00",40.7607,-73.9625,"B02512"
#
# ==> uber-raw-data-sep14.csv <==
# "Date/Time","Lat","Lon","Base"
# "9/1/2014 0:01:00",40.2201,-74.0021,"B02512"
# "9/1/2014 0:01:00",40.75,-74.0027,"B02512"
# "9/1/2014 0:03:00",40.7559,-73.9864,"B02512"
# "9/1/2014 0:06:00",40.745,-73.9889,"B02512"
# "9/1/2014 0:11:00",40.8145,-73.9444,"B02512"
# "9/1/2014 0:12:00",40.6735,-73.9918,"B02512"
# "9/1/2014 0:15:00",40.7471,-73.6472,"B02512"
# "9/1/2014 0:16:00",40.6613,-74.2691,"B02512"
# "9/1/2014 0:32:00",40.3745,-73.9999,"B02512"
# ```
#
# ## Description des données source
#
# Il y a trois types de fichier.
# Ceux de l'année 2014 qui ont tous la même structure csv en colonne : "Date/Time","Lat","Lon","Base" .
#
# Puis deux types de fichiers pour 2015.
# Le premier, taxi-zone-lookup.csv, contient la nomenclature des locationID des fcihiers des courses sur 2025 dans un format csv suivant les colonnes LocationID,Borough,Zone.
# LocationID est une sorte de clé étrangère dans le fichier des courses 2015 lié avec la colonne locationID.
#
# Enfin le fichier uber-raw-data-janjune-15.csv est un fichier csv énorme (~500 Mo) contenant les courses de 2015 sous un format colonne : Dispatching_base_num,Pickup_date,Affiliated_base_num,locationID.
#
#

# %% [markdown]
# 1. import the librairies for the project

# %%
import pandas as pd
import numpy as np

# import sklearn and plotly to visualize dataset
from sklearn.datasets import make_moons
from sklearn.model_selection import train_test_split
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import OneHotEncoder, StandardScaler, LabelEncoder
from sklearn.compose import ColumnTransformer
from sklearn.cluster import DBSCAN

# Import plotly
import plotly.express as px
import plotly.graph_objects as go
import plotly.io as pio

# setting Jedha color palette as default
pio.templates["jedha"] = go.layout.Template(
    layout_colorway=[
        "#4B9AC7",
        "#4BE8E0",
        "#9DD4F3",
        "#97FBF6",
        "#2A7FAF",
        "#23B1AB",
        "#0E3449",
        "#015955",
    ]
)
pio.templates.default = "jedha"
pio.renderers.default = "vscode"  # to be replaced by "iframe" if working on JULIE

# %% [markdown]
# 2. analyse sommaire des données.

# %%
from os import listdir, getcwd

getcwd()
files = listdir("./Data/2014")

dataframes = []
for file in files:
    print("fichier : ", file)
    dataframes.append(
        {
            "fichier": file.split(".")[0],
            "df": pd.read_csv("./Data/2014/" + file, nrows=10000),
        }
    )
    display(dataframes[-1]["df"].describe(include="all"))


def get_item(collection, key, target):
    # use 'generator'
    for dict_ in (x for x in collection if x[key] == "uber-raw-data-" + target):
        return dict_["df"]


# %%
df_2014 = pd.read_csv("./Data/2014/uber-raw-data-apr14.csv")
for ele in ["apr14", "may14", "jun14", "jul14", "aug14", "sep14"]:
    df_2014 = pd.concat([df_2014, get_item(dataframes, "fichier", ele)])

# %%
df_2015 = pd.read_csv("./Data/2015/uber-raw-data-janjune-15.csv")
df_2015

# %%
# finding out if there are any null values
print("2014 dataset")
print(f" null values per column : {df_2014.isnull().sum()}")
print(f" number of null values : {df_2014.isnull().sum().sum()}")
print(f"Dataset shape for 2014 : {df_2014.shape}")
display(df_2014.info())
display(df_2014.head())
display(df_2014.shape)
print("________________________________")
print("2015 dataset")
print(f" null values per column : {df_2015.isnull().sum()}")
print(f" number of null values : {df_2015.isnull().sum().sum()}")
print(f"Dataset shape for 2015 : {df_2015.shape}")
display(df_2015.info())
display(df_2015.head())
display(df_2015.shape)
print("________________________________")

# %%
df_sample = df_2014  # .sample(100000, random_state=42)

df_sample["Date/Time"] = pd.to_datetime(df_sample["Date/Time"])
df_sample["hour"] = df_sample["Date/Time"].dt.hour
df_sample["day_num"] = df_sample["Date/Time"].dt.dayofweek
df_sample["dayofweek"] = df_sample["Date/Time"].dt.day_name()
df_sample["quarter"] = df_sample["Date/Time"].dt.quarter
df_sample["month"] = df_sample["Date/Time"].dt.month
df_sample["year"] = df_sample["Date/Time"].dt.year
df_sample["dayofyear"] = df_sample["Date/Time"].dt.dayofyear
df_sample["dayofmonth"] = df_sample["Date/Time"].dt.day
df_sample["weekofyear"] = df_sample["Date/Time"].dt.isocalendar().week
df_sample.drop(columns=["Date/Time"], inplace=True)

display(df_sample.info())
display(df_sample.head())
print()


# %%
numeric_list = ["Lat", "Lon"]

for col in numeric_list:
    outliers = detect_outliers_iqr(df_sample, col)
    print(f"{col} -> Outlier : {outliers.shape[0]} with values :\n {outliers[col]}")
#
df_sample = df_sample.drop(outliers.index, axis=0)

display(df_sample)

# %%
df_sample_1 = df_2015  # .sample(300000, random_state=42)

df_sample_1["Pickup_date"] = pd.to_datetime(df_sample_1["Pickup_date"])
df_sample_1["hour"] = df_sample_1["Pickup_date"].dt.hour
df_sample_1["day_num"] = df_sample_1["Pickup_date"].dt.dayofweek
df_sample_1["dayofweek"] = df_sample_1["Pickup_date"].dt.day_name()
df_sample_1["quarter"] = df_sample_1["Pickup_date"].dt.quarter
df_sample_1["month"] = df_sample_1["Pickup_date"].dt.month
df_sample_1["year"] = df_sample_1["Pickup_date"].dt.year
df_sample_1["dayofyear"] = df_sample_1["Pickup_date"].dt.dayofyear
df_sample_1["dayofmonth"] = df_sample_1["Pickup_date"].dt.day
df_sample_1["weekofyear"] = df_sample_1["Pickup_date"].dt.isocalendar().week
df_sample_1.drop(columns=["Pickup_date"], inplace=True)

display(df_sample_1.info())
display(df_sample_1.head())
print()

# %%
df_sample_1.rename(columns={"Dispatching_base_num": "Base"}, inplace=True)
df_sample_1.drop(columns=["Affiliated_base_num"], axis=1, inplace=True)
df_sample_1

# %%
df_ny_tlc_zone = pd.read_csv("./Data/NYC_Taxi_Zones.csv")
df_ny_tlc_zone.info()


# %%
def get_region_center(multipolygon):
    tex = (
        multipolygon.replace("(", "")
        .replace(")", "")
        .replace("MULTIPOLYGON", "")
        .replace("))", "")
        .replace("), ((", "|")
        .replace(",", ";")
    )
    texts = tex[:-2].split(";")
    X = 0
    Y = 0
    n = len(texts)
    for ele in texts:
        coord = ele.split(" ")
        X += float(coord[1])
        Y += float(coord[2])
    reg = (X / n, Y / n)
    return reg


# %%

df_ny_tlc_zone["center"] = df_ny_tlc_zone["Shape Geometry"].apply(get_region_center)
df_ny_tlc_zone.index = df_ny_tlc_zone["Location ID"]
df_ny_tlc_zone["Lat"] = df_ny_tlc_zone["center"].apply(lambda x: x[1])
df_ny_tlc_zone["Lon"] = df_ny_tlc_zone["center"].apply(lambda x: x[0])
df_ny_tlc_zone = df_ny_tlc_zone[["Borough", "Zone", "Lat", "Lon"]]
new_rows = pd.DataFrame(
    {
        "Borough": ["Unknown", "Unknown"],
        "Zone": ["Unknown", "Unknown"],
        "Lat": [0.0, 0.0],
        "Lon": [0.0, 0.0],
    },
    index=[264, 265],
)
df_ny_tlc_zone = pd.concat([df_ny_tlc_zone, new_rows], ignore_index=False)
df_ny_tlc_zone

# %%
df_sample_1["Lat"] = df_sample_1["locationID"].apply(
    lambda x: df_ny_tlc_zone.loc[x]["Lat"]
)
df_sample_1["Lon"] = df_sample_1["locationID"].apply(
    lambda x: df_ny_tlc_zone.loc[x]["Lon"]
)
df_sample_1.drop(columns=["locationID"], inplace=True)
df_sample_1

# %%
numeric_list = ["Lat", "Lon"]

for col in numeric_list:
    outliers = detect_outliers_iqr(df_sample_1, col)
    print(f"{col} -> Outlier : {outliers.shape[0]} with values :\n {outliers[col]}")
outliers.index
df_sample_1 = df_sample_1.drop(outliers.index, axis=0)
display(df_sample_1)

# %%
# trying to find the number of months. There are 6 of them (april-sep) for 2014
print(df_sample["month"].unique().tolist())
print(df_sample["Base"].unique().tolist())
# same for 2015
print(df_sample_1["month"].unique().tolist())
print(df_sample_1["Base"].unique().tolist())

# %%
monthly_uber_rides_2014 = df_sample[["month", "Base"]].pivot_table(
    index=["month"], values="Base", aggfunc="count"
)
fig = px.bar(
    monthly_uber_rides_2014, x=monthly_uber_rides_2014.index, y="Base", title="2014"
)
fig.show()
monthly_uber_rides_2014

# %%
monthly_uber_rides_2014

# %%
daily_uber_rides_2014 = df_sample.pivot_table(
    index=["day_num", "dayofweek"], values="Base", aggfunc="count"
)
daily_uber_rides_2014.plot(
    kind="bar",
    figsize=(8, 6),
    ylabel="Total Journeys",
    xlabel="Days of the Week",
    title="2014",
    color="#4B9AC7",
)


# %%
daily_uber_rides_2015 = df_sample_1.pivot_table(
    index=["day_num", "dayofweek"], values="Base", aggfunc="count"
)
daily_uber_rides_2015.plot(
    kind="bar",
    figsize=(8, 6),
    ylabel="Total Journeys",
    xlabel="Days of the Week",
    title="2015",
    color="#4B9AC7",
)

# %%
## groupby operation 2014
daily_uber_rides_month_2014 = df_sample.groupby(["month", "day_num", "dayofweek"])[
    "Base"
].count()
daily_uber_rides_month_2014 = daily_uber_rides_month.reset_index()
daily_uber_rides_month_2014.head()

# %%
## groupby operation 2015
daily_uber_rides_month_2015 = df_sample_1.groupby(["month", "day_num", "dayofweek"])[
    "Base"
].count()
daily_uber_rides_month_2015 = daily_uber_rides_month_2015.reset_index()
daily_uber_rides_month_2015.head()

# %%
## create figure


ax = px.line(
    daily_uber_rides_month_2014,
    x="dayofweek",
    y="Base",
    color="month",
    labels={"dayofweek": "Day of Week", "Base": "Base", "month": "month"},
    title="Total Number of Pickups for Each Weekday per Month (April-September 2014)",
)
ax.show()
ax = px.line(
    daily_uber_rides_month_2015,
    x="dayofweek",
    y="Base",
    color="month",
    labels={"dayofweek": "Day of Week", "Base": "Base", "month": "month"},
    title="Total Number of Pickups for Each Weekday per Month (April-September 2015)",
)
ax.show()


# %%
uber_hour_2014 = df_sample.pivot_table(index="hour", values="Base", aggfunc="count")
fig = px.bar(
    uber_hour_2014,
    labels={"HourOfDay": "hour of the day", "Base": "Base", "count": "Total Journeys"},
    title="Journeys by Hour 2014",
)
fig.show()
uber_hour_2015 = df_sample_1.pivot_table(index="hour", values="Base", aggfunc="count")
fig = px.bar(
    uber_hour_2015,
    labels={"HourOfDay": "hour of the day", "Base": "Base", "count": "Total Journeys"},
    title="Journeys by Hour 2015",
)
fig.show()

# %%
df_sample, df_sample_1

# %%
df_2014_2015 = pd.concat([df_sample, df_sample_1], ignore_index=True, axis=0)

# %%
df_2014_2015

# %%

df_2014_2015.reset_index(inplace=True)
fig = px.scatter_map(
    df_2014_2015,
    lat="Lat",
    lon="Lon",
    color="dayofweek",
    title="2014-2015",
    zoom=8,
    animation_frame="year",
    map_style="open-street-map",
)

# %%
fig.show()

# %%
## get ride data
ride_data_2014 = df_sample
ride_data_2014 = df_sample.loc[
    (df_sample["dayofmonth"] == 21) & (df_sample["hour"] > 15)
]

## maximum distance between two cluster members in kilometers
max_distance = 0.05  # 0.05

## minimum number of cluster members
min_pickups = 25

## call the get_hot_spots function
hot_spots_2014 = get_hot_spots(max_distance, min_pickups, ride_data_2014)
hot_spots_2014

# %%
## set the color scale
color_scale = np.log(hot_spots_2014[2])
# color_scale = hot_spots[2]

fig_dbscan_hot_spots_2014 = px.scatter_map(
    lat=hot_spots_2014[0],
    lon=hot_spots_2014[1],
    color=color_scale,
    zoom=5,
    map_style="basic",
    title="Clusters of Uber Pickups Hot Spots on 2014",
)
# map_style (str (default 'basic')) – Identifier of base map style.
# Allowed values are    'basic', 'carto-darkmatter', 'carto-darkmatter-nolabels',
#                       'carto-positron', 'carto-positron-nolabels', 'carto-voyager',
#                        'carto-voyager-nolabels', 'dark', 'light',
#                        'open-street-map', 'outdoors', 'satellite',
#                        'satellite-streets', 'streets', 'white-bg'.
fig_dbscan_hot_spots_2014.show()


# %%


# %%
numeric_features = ["Lat", "Lon"]  # Positions des colonnes quantitatives dans X
category_feature = ["Base"]
df_sample = df_sample[df_sample["dayofweek"] == "Thursday"]

numeric_transformer = (
    StandardScaler()
)  ####### utile de standard scaler ? on perd pas de l'info sur la distance hmmm ?
category_transformer = OneHotEncoder(handle_unknown="ignore")

preprocessor = ColumnTransformer(
    transformers=[
        ("num", numeric_transformer, numeric_features),
        ("cat", category_transformer, category_feature),
    ],
    remainder="passthrough",
)


X_2014 = preprocessor.fit_transform(df_sample)


db = DBSCAN(eps=0.2, min_samples=10, metric="manhattan")

db.fit(X_2014)

# %%
np.unique(db.labels_)
df_sample["cluster"] = db.labels_
df_sample.head()

# %%
fig_dbscan_2014 = px.scatter_map(
    df_sample[df_sample["cluster"] > -1],
    lat="Lat",
    lon="Lon",
    color="cluster",
    zoom=7,
    map_style="carto-positron",
    title="Clusters of Uber Pickups on Saturdays",
)

fig_dbscan_2014.show()

# %% [markdown]
# ## 2015
#

# %%
## get ride data
ride_data_2015 = df_sample_1.loc[
    (df_sample["dayofmonth"] == 21) & (df_sample["hour"] > 15)
]

## maximum distance between two cluster members in kilometers
max_distance = 0.05

## minimum number of cluster members
min_pickups = 25

## call the get_hot_spots function
hot_spots_2015 = get_hot_spots(max_distance, min_pickups, ride_data_2015)

# %%
## set the color scale
color_scale = np.log(hot_spots_2015[2])
# color_scale = hot_spots[2]

fig_dbscan_hot_spots_2015 = px.scatter_mapbox(
    lat=hot_spots_2015[0],
    lon=hot_spots_2015[1],
    color=color_scale,
    zoom=7,
    mapbox_style="carto-positron",
    title="Clusters of Uber Pickups Hot Spots on 2015",
)

fig_dbscan_hot_spots_2015.show()


# %%
numeric_features = ["Lat", "Lon"]  # Positions des colonnes quantitatives dans X
df_sample = df_sample[df_sample_1["dayofweek"] == 5]

numeric_transformer = (
    StandardScaler()
)  ####### utile de standard sclaer ? on perd pas de l'info sur la distance hmmm ?


preprocessor = ColumnTransformer(
    transformers=[
        ("num", numeric_transformer, numeric_features),
    ],
    remainder="passthrough",
)


X_2015 = preprocessor.fit_transform(df_sample_1)

from sklearn.cluster import DBSCAN

db = DBSCAN(eps=0.2, min_samples=10, metric="manhattan")

db.fit(X_2015)

np.unique(db.labels_)
df_sample_1["cluster"] = db.labels_
df_sample_1.head()

fig_dbscan_2015 = px.scatter_mapbox(
    df_sample_1[df_sample_1["cluster"] > -1],
    lat="Lat",
    lon="Lon",
    color="cluster",
    zoom=7,
    mapbox_style="carto-positron",
    title="Clusters of Uber Pickups on Saturdays",
)

fig_dbscan_2015.show()

# %% [markdown]
#

# %% [markdown]
# ## Essai avec le K-Means pour faire des clusters

# %%
# Import K-Means
from sklearn.cluster import KMeans

# Instanciate KMeans with k=3 and initialisation with k-means++
# You should always use k-means++ as it alleviate the problem of local minimum convergence
kmeans = KMeans(n_clusters=5, random_state=0)

# Fit kmeans to our dataset
kmeans.fit(X_2014)
cluster = kmeans.predict(X_2014)
df_sample["cluster-kmeans"] = pd.DataFrame(cluster, columns=["cluster"])
df_sample.head(30)
cluster
print()
fig = px.scatter_mapbox(
    df_sample,
    lat="Lat",
    lon="Lon",
    color="cluster-kmeans",
    zoom=6,
    mapbox_style="carto-positron",
)

fig.show()

# %%
# Let's create a loop that will collect the Within-sum-of-square (wcss) for each value K
# Let's use .inertia_ parameter to get the within sum of square value for each value K
wcss = []
k = []
for i in range(1, 11):
    kmeans = KMeans(n_clusters=i, random_state=0, n_init="auto")
    kmeans.fit(X)
    wcss.append(kmeans.inertia_)
    k.append(i)
    print("WCSS for K={} --> {}".format(i, wcss[-1]))

# %%
# Create DataFrame
wcss_frame = pd.DataFrame(wcss)
k_frame = pd.Series(k)

# Create figure
fig = px.line(wcss_frame, x=k_frame, y=wcss_frame.iloc[:, -1])

# Create title and axis labels
fig.update_layout(
    yaxis_title="Inertia", xaxis_title="# Clusters", title="Inertia per cluster"
)

# Render
# fig.show(renderer="notebook")
fig.show()  # if using workspace

# %%
# Import silhouette score
from sklearn.metrics import silhouette_score

# Computer mean silhouette score
sil = []
k = []

## Careful, you need to start at i=2 as silhouette score cannot accept less than 2 labels
for i in range(2, 11):
    kmeans = KMeans(n_clusters=i, random_state=0, n_init="auto")
    kmeans.fit(X)
    sil.append(silhouette_score(X, kmeans.predict(X)))
    k.append(i)
    print("Silhouette score for K={} is {}".format(i, sil[-1]))

# %%
# Create a data frame
cluster_scores = pd.DataFrame(sil)
k_frame = pd.Series(k)

# Create figure
fig = px.bar(data_frame=cluster_scores, x=k, y=cluster_scores.iloc[:, -1])

# Add title and axis labels
fig.update_layout(
    yaxis_title="Silhouette Score",
    xaxis_title="# Clusters",
    title="Silhouette Score per cluster",
)

# Render
# fig.show(renderer="notebook")
fig.show()  # if using workspace

# %%
