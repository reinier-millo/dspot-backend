#!/bin/bash

if test -d _python; then
    source _python/bin/activate
fi

# Get files from git commit or use all py files
files="$@"
if [ -z "$files" ]; 
then
    files="**/*.py \
    app/**/*.py \
    app/routes/v1/*.py \
    tests/*.py"
fi

if [ ! -e ".env" ]; then
    cp .env.example .env
fi

echo "Running autopep8 on: $files"
autopep8 --in-place --recursive $files

pylint --rcfile=.pylintrc $files