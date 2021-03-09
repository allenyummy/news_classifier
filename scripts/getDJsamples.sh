#!/bin/bash

# Copy random 10 news from $DJPATH

DJPATH=../DataSets/dowjones-news/news/zhtw
DJLOCAL=news_samples/dowjones/

mkdir -p $DJLOCAL

for fn in $(ls $DJPATH | sort -R | tail -10)
do
    echo "$DJPATH/$fn -> $DJLOCAL"
    cp $DJPATH/$fn $DJLOCAL
done