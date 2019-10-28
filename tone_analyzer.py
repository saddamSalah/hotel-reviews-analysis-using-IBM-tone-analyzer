from flask import Flask, request, jsonify
import pandas as pd
from ibm_watson import ToneAnalyzerV3
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator

from ibm_watson import ApiException

authenticator = IAMAuthenticator('m6OQaGvToZE0deKEi_GDSfcTMYPr6ijJChenY1Er9Jvq')
tone_analyzer = ToneAnalyzerV3(
    version='2019-10-24',
    authenticator=authenticator
)

tone_analyzer.set_service_url('https://gateway-lon.watsonplatform.net/tone-analyzer/api')
tone_analyzer.set_disable_ssl_verification(True)
app = Flask('tone_analyzer')


def get_unique_tones(tones):
    tones_names = []
    for tone in tones:
        doc_tone = tone['document_tone']
        tones = doc_tone['tones']
        for val in tones:
            tones_names.append(val['tone_name'])
    return list(set(tones_names))


def normalize_tone_values(unique_tones, tones):
    data = {}
    for unique_value in unique_tones:
        c = 0
        score= 0
        for doc_tone in tones:
            summary = doc_tone['document_tone']
            tone_summary = summary['tones']
            for i in tone_summary:
                if i['tone_name'] == unique_value:
                    c = c +1
                    score = score + i['score']
        score = score / c
        data[unique_value] = score
    return data


@app.route('/analyzer', methods=['GET', 'POST'])
def analyze_reviews():
    try:
        tones = []
        content = request.get_json(force=True)
        reviews = content['reviews']
        for i in range(3):
            tone_analysis = tone_analyzer.tone(
                {'text': reviews[i]},
                content_type='text/plain',
                sentences=False
            ).get_result()
            tones.append(tone_analysis)
    except ApiException as ex:
        print("Method failed with status code " + str(ex.code) + ": " + ex.message)
    unique_tones = get_unique_tones(tones)
    return normalize_tone_values(unique_tones, tones)


if __name__ == '__main__':
    app.run(debug=True, port=7000)
