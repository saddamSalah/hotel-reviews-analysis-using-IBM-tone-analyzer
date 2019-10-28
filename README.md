# hotel-reviews-analysis-using-IBM-tone-analyzer
First,run preprocess.py to filter the full dataset and get only hotels data.
run tone_analyzer.py to start the app, that receive hotel by hotel reviews and return normalized score of the tones in it. 
run hotel indexer.py that manges the process which fetch the dataset and read the data of hotel by hotel, then send http request to the tone analyzer micro services to clacluate the normalized score, then it recives the response which appended in the document of that hotel to be indexed in elastic search.
Each hotel is indexed in only one document that ibncludes the original data from the dataset and the data the returned from the IBM watson tone analyzer.
Notes
  - We procress only 3 reviews for each hotel to prove the concept using the free quote of IBM watson tone analyzer
  - To edit the the tone analyzer microservice to apply the process for all of the reviews of each hotel you need to:
      - edit IAMAuthenticator in tone_analyzer.py to use your access token
      - edit analyze_reviews method in the same script to let the for loop to loop over the (len(reviews))
      
