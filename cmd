#!/bin/bash
rm -f xkcd.zip && zip -j xkcd.zip comics/* && cd comics && ebook-convert ../xkcd.zip ../xkcd.mobi --output-profile kindle --margin-top 0 --margin-bottom 0 --margin-left 0
