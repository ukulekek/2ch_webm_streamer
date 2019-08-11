#!/bin/bash
    

    #if [ $1 = '-h' -o $1 = '--help' ]; then echo "Usage: ./stream.sh [URL] -p [PLAYER]"; exit 1;fi 
    #if [ $# -ne 3 ]; then echo "Arguments error" >&2; exit 1; fi

   # curl $1 -o thread_copy || echo "URL error" >&2||exit 1
    
parse_b() {
    # curl https://2ch.hk/b/catalog.json -o catalog.json 
    jq '.threads[] | {num: .num, subject: .subject, files_count: .files_count} | select(.subject|test("[WwMm][EePp][Bb4][Mm]"))' catalog.json > parsed_b.json
    sed -i '1s/^/\[/' parsed_b.json
    sed -i 's/\}/},/' parsed_b.json
    sed -i '$s/},/}\]/' parsed_b.json
}

print_threads() {
    THREAD_CNT=0
    for thread in $( grep -o 'subject' parsed_b.json)
    do
	    echo "Thread #${THREAD_CNT}"
	    jq ".[${THREAD_CNT}]" parsed_b.json
	    THREAD_CNT=$(( $THREAD_CNT + 1 ))
    done
}

download_thread() {
    echo 'Choose your thread (print a number):'
    read THREAD
    curl https://2ch.hk/b/res/`jq --raw-output ".[$THREAD][\"num\"]" parsed_b.json`.json > thread_copy.json

}

create_playlist() {
    echo "#EXTM3U" > playlist.m3u || echo "Creating playlist error"|| exit 1
    COUNTER=1
    for link in $( grep -o '\/[a-z]*\/src\/[0-9]*\/[0-9]*\.[wm][ep][b4][m]*' thread_copy.json |uniq)
    do
        echo -e "#EXTINF:-1, Video:$COUNTER\nhttps://2ch.hk/$link\n\n" >> playlist.m3u
        COUNTER=$(( $COUNTER + 1 ))
    done
    echo success
}

clean() {
    rm -rf catalog.json pared_b.json thread_copy.json
}
parse_b
print_threads
download_thread
create_playlist

