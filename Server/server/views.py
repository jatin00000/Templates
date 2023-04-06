import os
from http import HTTPStatus
import json
import http.client
import base64
from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from dotenv import load_dotenv
load_dotenv()


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token['username'] = user.username
        # ...

        return token


class MyTokenObtainPairView(TokenObtainPairView):

    serializer_class = MyTokenObtainPairSerializer


class start(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        if request.user.is_authenticated:
            # User is authenticated, proceed with processing the request
            payload = { "query": { "match_all": {} }, "aggs": { "logs_by_date": { "date_histogram": { "field": "timestamp", "calendar_interval": "day" }, "aggs": { "total_logs": { "value_count": { "field": "@timestamp" } }, "status_code_counts": { "terms": { "field": "status_code" } }, "type_counts": { "terms": { "field": "type" } } } } } }
            # a = json.loads(database("POST", payload))
            a = databaseNew(payload)
            buckets = a["aggregations"]["logs_by_date"]["buckets"]
            res = []
            for item in buckets:
                if item["doc_count"]>0:
                    res.append({"date": str(item["key_as_string"]).split(" ")[0], "total_logs": item["doc_count"], "type": {i["key"]: i["doc_count"]
                                                                                                                        for i in item["type_counts"]["buckets"]}, "status_code": {i["key"]: i["doc_count"] for i in item["status_code_counts"]["buckets"]}})
            return JsonResponse({"list": res})
        else:
            # User is not authenticated, return 401 Unauthorized response
            return Response(status=HTTPStatus.UNAUTHORIZED)


class start_date(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        if request.user.is_authenticated:
            # User is authenticated, proceed with processing the request
            payload = {"size": 0,"aggs": {"logs_by_day": {"date_histogram": {"field": "timestamp","calendar_interval": "day"}}}}
            # a = json.loads(database("POST", payload))
            a = databaseNew(payload)
            buckets = a["aggregations"]["logs_by_day"]["buckets"]
            res = []
            for item in buckets:
                s = item["key_as_string"]
                res.append(str(s).split(" ")[0])
            return JsonResponse({"list": res})
        else:
            # User is not authenticated, return 401 Unauthorized response
            return Response(status=HTTPStatus.UNAUTHORIZED)


class start_status(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        if request.user.is_authenticated:
            # User is authenticated, proceed with processing the request
            payload = {"size": 0,"aggs": {"status_codes": {"terms": {"field": "status_code"}}}}
            # a = json.loads(database("POST", payload))
            a = databaseNew(payload)
            buckets = a["aggregations"]["status_codes"]["buckets"]
            res = []
            for item in buckets:
                res.append(item["key"])
            return JsonResponse({"list": res})
        else:
            # User is not authenticated, return 401 Unauthorized response
            return Response(status=HTTPStatus.UNAUTHORIZED)


class start_type(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        if request.user.is_authenticated:
            payload = {"size": 0,"aggs": {"type": {"terms": {"field": "type"}}}}
            # a = json.loads(database("POST", payload))
            a = databaseNew(payload)
            buckets = a["aggregations"]["type"]["buckets"]
            res = []
            for item in buckets:
                res.append(item["key"])
            return JsonResponse({"list": res})
        else:
            # User is not authenticated, return 401 Unauthorized response
            return Response(status=HTTPStatus.UNAUTHORIZED)


class search(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        if request.user.is_authenticated:
            payload = { "query": { "match_all": {} }, "aggs": { "logs_by_date": { "date_histogram": { "field": "timestamp", "calendar_interval": "day" }, "aggs": { "total_logs": { "value_count": { "field": "@timestamp" } }, "status_code_counts": { "terms": { "field": "status_code" } }, "type_counts": { "terms": { "field": "type" } } } } } }
            # a = json.loads(database("POST", payload))
            a = databaseNew(payload)
            buckets = a["aggregations"]["logs_by_date"]["buckets"]
            res = []

            # extract date and status_code lists from request
            request_data = json.loads(request.body)
            date_list = request_data.get("date", [])
            status_code_list = request_data.get("status_code", [])
            type_list = request_data.get("type", [])
            for item in buckets:
                listStatus, listType, count = {}, {}, item["doc_count"]

                # check if item date is in date_list
                if not date_list or str(item["key_as_string"]).split(" ")[0] in date_list:

                    # filter status_code by status_code_list
                    for i in item["status_code_counts"]["buckets"]:
                        if not status_code_list or i["key"] in status_code_list:
                            listStatus[i["key"]] = i["doc_count"]
                            

                    # filter type by type_list
                    for i in item["type_counts"]["buckets"]:
                        if not type_list or i["key"] in type_list:
                            listType[i["key"]] = i["doc_count"]

                    # append to result list
                    if count>0:
                        res.append({"date": str(item["key_as_string"]).split(" ")[0], "total_logs": count, "type": listType, "status_code": listStatus})

            return JsonResponse({"list": res})
        else:
            # User is not authenticated, return 401 Unauthorized response
            return Response(status=HTTPStatus.UNAUTHORIZED)


def database(method, payload):
    conn = http.client.HTTPSConnection( 
        os.getenv('ESADDRESS'), os.getenv('PORT'))
    uname = os.getenv('NAME')
    password = os.getenv('PASSWORD')
    auth_str = f'{uname}:{password}'
    print(uname)
    byte_str = auth_str.encode('ascii')
    auth_b64 = base64.b64encode(byte_str)

    headersList = {
        "Content-Type": "application/json",
        "Authorization": "Basic %s" % auth_b64.decode(),
        "Content-Type": "application/json"
    }
    conn.request(method, "/index_/_search", payload, headersList)
    response = conn.getresponse()
    result = response.read().decode('utf-8')
    return result

from time import sleep
from elasticsearch import helpers, Elasticsearch
import pandas as pd
import csv
from datetime import datetime

def dataEditer(df):
    es = Elasticsearch(hosts=[os.getenv('ESSERVER')])
    if not es.indices.exists(index=os.getenv('INDEXNAME')):
        temp = {"properties": {"status_code": {"type": "long"},"timestamp": {"type": "date_nanos","format": "yyyy-MM-dd HH:mm:ss.SSSSSS"},"type": {"type": "keyword"},"url": {"type": "text"}}}
        es.indices.create(index=os.getenv('INDEXNAME'), mappings=temp, settings={})
    # Load csv data into a pandas DataFrame
    

    # drop any row with an empty column
    df.dropna(inplace=True)

    # iterate over each row/item in the DataFrame and transform it into a dictionary
    upload_list = []
    for index, row in df.iterrows():

        item_dict = {}

        # transform data from the row into a dictionary item
        dt_object = datetime.strptime(row[0], '%Y-%m-%d %H:%M:%S.%f')
        item_dict["timestamp"] = dt_object.strftime('%Y-%m-%d 00:00:00.000000')
        item_dict["url"] = row[1]
        item_dict["status_code"] = row[2]
        item_dict["type"] = row[3]

        # add the transformed item/row to a list of dicts
        upload_list.append(item_dict) 
    helpers.bulk(es, upload_list, index=os.getenv('INDEXNAME'))
    sleep(3)
try:
    df = pd.read_csv('server\LogFiles\_init_.csv')
    dataEditer(df)
    os.rename('server\LogFiles\_init_.csv','server\LogFiles\_init_done.csv')
except FileNotFoundError:
    pass
def databaseNew(payload):
    es = Elasticsearch(hosts=[os.getenv('ESSERVER')])
    if not es.indices.exists(index=os.getenv('INDEXNAME')):
        temp = {"properties": {"status_code": {"type": "long"},"timestamp": {"type": "date_nanos","format": "yyyy-MM-dd HH:mm:ss.SSSSSS"},"type": {"type": "keyword"},"url": {"type": "text"}}}
        es.indices.create(index=os.getenv('INDEXNAME'), mappings=temp, settings={})
    response = es.search(index=os.getenv('INDEXNAME'), body=payload )
    return response
