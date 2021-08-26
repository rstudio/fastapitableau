#! /usr/env bash


# Regular-style requests

curl -X 'POST' \
'http://127.0.0.1:8000/capitalize' \
-H 'accept: application/json' \
-H 'Content-Type: application/json' \
-d '[
        "dog",
        "cat",
        "rabbit"
]'


curl -X 'POST' \
'http://127.0.0.1:8000/paste' \
-H 'accept: application/json' \
-H 'Content-Type: application/json' \
-d '{
        "first": ["Toph", "Bill", "James"],
        "second": ["Allen", "Sager", "Blair"]
}'


# Tableau-style requests

curl -X 'POST' \
'http://127.0.0.1:8000/evaluate' \
-H 'accept: application/json' \
-H 'Content-Type: application/json' \
-d '{
        "script": "/capitalize",
        "data": {   
                "arg1_": ["dog", "cat", "rabbit"]
        }
}'


curl -X 'POST' \
'http://127.0.0.1:8000/evaluate' \
-H 'accept: application/json' \
-H 'Content-Type: application/json' \
-d '{
        "script": "/paste",
        "data": {   
                "arg1_": ["Toph", "Bill", "James"],
                "arg2_": ["Allen", "Sager", "Blair"]
        }
}'


# Bad requests

# Malformed paste request — too few args
curl -X 'POST' \
'http://127.0.0.1:8000/paste' \
-H 'accept: application/json' \
-H 'Content-Type: application/json' \
-d '{
        "first": ["Toph", "Bill", "James"],
}'


# Malformed paste request — too few args
curl -X 'POST' \
'http://127.0.0.1:8000/paste' \
-H 'accept: application/json' \
-H 'Content-Type: application/json' \
-d '{
        "first": ["Toph", "Bill", "James"],
}'


# Empty request to evaluate
curl -X 'POST' \
'http://127.0.0.1:8000/evaluate' \
-H 'accept: application/json' \
-H 'Content-Type: application/json'
