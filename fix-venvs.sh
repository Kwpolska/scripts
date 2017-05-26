#!/bin/zsh
for dir in */; do
    if [[ ! -d $dir ]]; then
        continue
    fi
    if [[ -e $dir/bin/python2 ]]; then
        interpreter=python2
    else
        interpreter=python3
    fi
    find $dir -type l -delete
    virtualenv -p /usr/local/bin/$interpreter $dir
done
