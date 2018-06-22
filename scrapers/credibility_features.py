#! usr/bin/env python

import sys
import codecs
import ast
from datetime import datetime
from scrapers.page_rank import PageRank
from scrapers.tweeter_metrics import ExtractAuthFeatures
from scrapers.environments import THRESHOLD_URL
import scrapers.web_trust_score as wts


class CredFeatures(object):

    def __init__(self):
        self.__avail_scores = '../data/available_scores'
        self.__threshold_score = '../data/threshold_score'
        self.pr = PageRank()
        self.twit_feat = ExtractAuthFeatures()

    def get_features(self, query):
        with codecs.open(self.__avail_scores, 'r', 'utf-8') as available_scores:
            for line in available_scores:
                tokens = line.split('|')
                if tokens[0] == str(datetime.today().date()):
                    if tokens[1] == query.strip().lower():
                        return ast.literal_eval(tokens[2])
        scores = wts.get_rank(query)
        for key, value in self.pr.get_rank(query).items():
            scores[key] = value
        for key, value in self.twit_feat.get_tweets(query).items():
            scores[key] = value
        with codecs.open(self.__avail_scores, 'a', 'utf-8') as write_scores:
            write_scores.write(str(datetime.today().date())+'|'+str(query.strip().lower()) + '|' + str(scores)+'\n')
        return scores

    def send_format(self, scores):
        """
        Normalized with google scores
        :param scores:
        :return:
        """
        print(float(self.emptytozero(scores['Backlinks'].strip().replace(',',''))))
        with codecs.open(self.__threshold_score, 'r', 'utf-8') as thresholding:
            for line in thresholding:
                tokens = line.split('|')
                threshold_scores = ast.literal_eval(tokens[2])
                break
        print(float(self.emptytozero(threshold_scores['Backlinks'].strip().replace(',',''))))
        favorite_count = scores['favourites_count']*100/threshold_scores['favourites_count']
        Backlinks = float(self.emptytozero(scores['Backlinks'].strip().replace(',','')))*100/float(self.emptytozero(threshold_scores['Backlinks'].strip().replace(',','')))
        friends_count = float(scores['friends_count'])*100/float(threshold_scores['friends_count'])
        google_pagerank = float(scores['Google PageRank'].split('/')[0])*10
        cPR_Score = float(scores['cPR Score'].split('/')[0])*10
        followers_count = float(scores['followers_count'])*100/float(threshold_scores['followers_count'])
        citations = float(scores['Citations'])*100/float(threshold_scores['Citations'])
        WOT_Score = float(scores['WOT Score'].split('/')[0])
        listed_count = float(scores['listed_count'])*100/float(threshold_scores['listed_count'])

        return {'nutrition': [
                {
                    "name": "favourites_count",
                    "display": "favourites_count: " + str(round(favorite_count)) + "%",
                    "value": favorite_count,
                    "percentage": favorite_count,
                    "color": "#f00"
                },
                {
                    "name": "Backlinks",
                    "display": "Backlinks: " + str(round(Backlinks)) + "%",
                    "value": Backlinks,
                    "percentage": Backlinks,
                    "color": "#0f0"
                },
                {
                    "name": "friends_count",
                    "display": "friends_count: " + str(round(friends_count)) + "%",
                    "value": friends_count,
                    "percentage": friends_count,
                    "color": "#0cc"
                },
                {
                    "name": "Google PageRank",
                    "display": "friends_count: " + str(round(google_pagerank)) + "%",
                    "value": google_pagerank,
                    "percentage": google_pagerank,
                    "color": "#0bc"
                },
                {
                    "name": "cPR_Score",
                    "display": "cPR_Score: " + str(round(cPR_Score)) + "%",
                    "value": cPR_Score,
                    "percentage": cPR_Score,
                    "color": "#0dc"
                },
                {
                    "name": "followers_count",
                    "display": "followers_count: " + str(round(followers_count)) + "%",
                    "value": followers_count,
                    "percentage": followers_count,
                    "color": "#0ec"
                },
                {
                    "name": "citations",
                    "display": "citations: " + str(round(citations)) + "%",
                    "value": citations,
                    "percentage": citations,
                    "color": "#0be"
                },
                {
                    "name": "WOT_Score",
                    "display": "WOT_Score: " + str(round(WOT_Score)) + "%",
                    "value": WOT_Score,
                    "percentage": WOT_Score,
                    "color": "#0fc"
                },
                {
                    "name": "listed_count",
                    "display": "listed_count: " + str(round(listed_count)) + "%",
                    "value": listed_count,
                    "percentage": listed_count,
                    "color": "#0ac"
                },
            ]}

    def emptytozero(self,input_string):
        if input_string == '':
            return '0'
        else:
            return input_string


def main():
    cred_obj = CredFeatures()
    scores =cred_obj.get_features(sys.argv[1])
    for key, value in scores.items():
        print("{}:{}".format(key, value))


if __name__ == '__main__':
    main()

