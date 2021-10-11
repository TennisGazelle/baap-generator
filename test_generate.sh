#!/bin/bash

IS_LOCAL=0

if [[ $IS_LOCAL -eq 1 ]]; then
    # Is Server running?
    echo "====> Validating that 'main.py' is running"
    if [[ $(ps -ef | grep src/main | grep -v grep) ]]; then
    # if [[ $(ls -A) ]]; then
        echo "====> it is running!"
    else
        echo "====> please run 'python3 validator.py' in a background shell!"
        exit 1
    fi

    URL=localhost:5000
else
    URL=https://baap-workdir-generator-auahkugdnq-uw.a.run.app
fi

echo $URL

# put in the good config
rm -rf response.zip
echo "====> fetching with specified 'config.yaml'"
curl -XPOST $URL/generate --form 'payload=@"./test/config.yaml"'  -o response.zip
echo "====> extracting 'config.yaml' from the downloaded file"
unzip -d tempdir -o response.zip
# diff -y tempdir/tempdir/*-baap/config.yaml test/config.yaml

# # put in the good config
# rm -rf response.zip
# echo "====> fetching with specified 'complex_config.yaml'"
# curl -XPOST localhost:5000/generate -d ‘@$(pwd)/test/complex_config.yaml’  -o response.zip
# echo "====> extracting 'config.yaml' from the downloaded file"
# unzip -d tempdir -o response.zip
# diff -y tempdir/TennisGazelle-*/config.yaml test/complex_config.yaml

exit 0