#!/bin/bash

KINOPOISKUSERID=247391
XLSFILENAME="rates.xls"
MOVIESFILENAME="rates.dat"
LINKSFILENAME="movies.links"
ENV="/usr/bin/env"
PYTHON="`which python`"

wget http://www.kinopoisk.ru/level/79/user/$KINOPOISKUSERID/votes/list/export/xls/  --header='User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:9.0.1) Gecko/20100101 Firefox/9.0.1' -O $XLSFILENAME
$PYTHON parser.py $XLSFILENAME="rates.xls" > $MOVIESFILENAME

IFS=$'\n'
for line in `cat $MOVIESFILENAME`; do
	link=`$PYTHON imdb_find_movie.py "$line"`
	movie="`echo $line | sed \"s/\*.*//\"`"
	if [ -z "$link" ] ; then
		echo "movie" $movie "not found; see error.log for details" 
	else
		rate="`echo $line | tr '*' '\n' | sed -n 9p`"
		$PYTHON imdb_rate_movie.py $link $rate
		echo $movie "OK"
	fi
done

rm -rf $XLSFILENAME $MOVIESFILENAME $LINKSFILENAME
