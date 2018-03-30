#!/bin/zsh
# Idea by @ilovezfs
for dir in */; do
    if [[ ! -d $dir ]]; then
        continue
    fi
    if [[ -e $dir/bin/python2 ]]; then
        interpreter=2
    else
        interpreter=3
    fi
rm $dir/.Python
ln -s /usr/local/opt/python/Frameworks/Python.framework/Versions/$interpreter.*/Python $dir/.Python
echo /usr/local/opt/python/Frameworks/Python.framework/Versions/$interpreter.* > $dir/lib/python$interpreter*/orig-prefix.txt
done
