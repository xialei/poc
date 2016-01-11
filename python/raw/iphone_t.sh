cat www_access.log |grep "/app/Yhyc.apk"|grep "$1"|grep "$2"|grep iPhone|awk '{print $1}'|uniq -c|sort -n -r|wc -l
