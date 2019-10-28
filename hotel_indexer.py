from flask import Flask, request, jsonify
from elasticsearch import Elasticsearch
import pandas as pd
import requests
import json
es = Elasticsearch()
app = Flask('hotel_indexer')
hotels = pd.read_csv('Data/hotels.csv')
hotels_names = hotels['name']
hotels_names = list(set(hotels_names))


def get_hotel_review(hotel_name):
    hotel_data = hotels.loc[hotels['name'] == hotel_name]
    reviews = hotel_data['reviews.text']
    return reviews


@app.route('/indexer', methods=['GET', 'POST'])
def send_review_to_analyzer():

    id = 0
    for hotel_name in hotels_names:

        hotel_data = hotels.loc[hotels['name'] == hotel_name]
        reviews = hotel_data['reviews.text']
        data = {}
        reviews = reviews.to_numpy()
        reviews = reviews.tolist()
        data['reviews'] = reviews
        json_data = json.dumps(data)
        normalized_tone_score = requests.post(url='http://127.0.0.1:7000/analyzer', data=json_data)
        document = {}
        document['address'] = hotel_data['address'].iloc[0]
        document['categories'] = hotel_data['categories'].iloc[0]
        document['city'] = hotel_data['city'].iloc[0]
        document['country'] = hotel_data['country'].iloc[0]
        document['latitude'] = hotel_data['latitude'].iloc[0]
        document['longitude'] = hotel_data['longitude'].iloc[0]
        document['name'] = hotel_data['name'].iloc[0]
        document['postalCode'] = hotel_data['postalCode'].iloc[0]
        document['province'] = hotel_data['province'].iloc[0]
        document['reviews.date'] = hotel_data['reviews.date'].to_json()
        document['reviews.date'] = hotel_data['reviews.date'].to_json()
        document['reviews.rating'] = hotel_data['reviews.rating'].to_json()
        document['reviews.text'] = hotel_data['reviews.text'].to_json()
        document['tone.analysis'] = normalized_tone_score.content
        try:
            es.index(index='hotels', id=id, doc_type='hotel_data', body=document)
            id = id + 1
        except:
            pass
    res = es.search(index='hotels', body={"from":0, "size":299, "query":{"match_all":{}}})
    return res


if __name__ == '__main__':
    app.run(debug=True, port=8000)


