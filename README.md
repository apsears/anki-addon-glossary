# anki-addon-glossary
Export an Anki desk as an Html Glossary automatically when syncing. 

It is based on https://ankiweb.net/shared/info/2751403243

## Description

Anki is a program for optimizing flashcard studying.  This project creates and exports an HTML table with your next N scheduled Anki cards, to facilitate offline studying and cramming.

It can also upload this table to an Amazon S3 bucket to ensure it is available for you on the go.

## Setup

Place ExportScheduled.py in your Anki addon folder, where it will be executed every time Anki syncs to AnkiWeb -- generally upon opening and closing.

## S3 Setup

If you wish to export the vocabulary table to an S3 bucket, take the following additional steps:

1) Install amazon cli tools: "pip install awscli"  
2) Configure S3 uploads with your Secret Keys: "aws configure"  
3) Create a system environment variable named S3BUCKET with then name of your bucket, like "MyVocabBucket"  
4) Uncomment the environment variable retrieval at the beginning and the shell call at the end of ExportScheduled.py  
