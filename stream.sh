#!/bin/bash
    

    if [ $1 = '-h' -o $1 = '--help' ]; then echo "Usage: ./stream.sh [URL] -p [PLAYER]"; exit 1;fi 
    if [ $# -ne 3 ]; then echo "Arguments error" >&2; exit 1; fi

    curl $1 -o thread_copy || echo "URL error" >&2||exit 1
    
    echo "#EXTM3U" > playlist.m3u || echo "Creating playlist eror"|| exit 1
    COUNTER=1
    for link in $( grep -o '\/[a-z]*\/src\/[0-9]*\/[0-9]*\.[wm][ep][b4][m]*' thread_copy |uniq)
    do
        echo -e "#EXTINF:-1, Video:$COUNTER\nhttps://2ch.hk/$link\n\n" >> playlist.m3u
        COUNTER=$(( $COUNTER + 1 ))
    done
    echo success
    $3 playlist.m3u
    

