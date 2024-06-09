# SPOTIFY PROJECT
At the beginning, data was retrieved from the Spotify API using the Spotipy library.
This project consists of three parts:

## 1. SONG POPULARITY PREDICTION
Based on features such as energy, liveness, tempo, duration, etc., we predict whether a song will become popular on Spotify or not.
Methods used for prediction:
### Linear Regression, Polynomial Regression, Random Forest, XGBOOST, MLP.
Then, an application was created to quickly see if a song will achieve commercial success by entering its details. The Streamlit library was used to create the application.
Link to check how the application works:  https://drive.google.com/file/d/1sMoD6Mdwt0KqT4vqjPWnhkq4j_ClraS5/view?usp=sharing
## 2. MUSIC GENRE CLASSIFICATION
The next part of the project was to see if we could determine the genre of a song using the available features from the data. This task proved to be challenging, as Spotify does not assign only one genre to a song.
When retrieving the data, only the first genre on the list of a song's genres was taken, so the classification was not very effective. The results of the classifiers were unsatisfactory. Accuracy was around 50-60%.
Methods used for classification:
### SVC, Random Forest, Logistic Regression, MLP, XGBOOST, KNN
## 3. SONG RECOMMENDATION
The last part involved recommending new songs to the user after they provided a link to their favorite playlist.
First, the songs were clustered, and then the user's playlist was averaged and assigned to a specific cluster. Within the cluster, songs with the highest cosine similarity coefficient were searched for.
Methods used:
### Cosine similarity, KMeans
Link to check how the application works: https://drive.google.com/file/d/1UDSRxT7zNOUmGk5ukGuYdejaHRtTibEg/view?usp=sharing

