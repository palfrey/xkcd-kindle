#!/bin/bash
zip xkcd.zip comics/* && ebook-convert xkcd.zip xkcd.mobi --output-profile kindle -d debug --margin-top 0 --margin-bottom 0 --margin-left 0
