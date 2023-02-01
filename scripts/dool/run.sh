#!/bin/sh
python3 dool --cpu-use --mem --net --disk --epoch --nocolor --noheaders --integer 5 | bash convert.sh
