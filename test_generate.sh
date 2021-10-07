#!/bin/bash

# Is Server running?

echo "====> Validating that 'main.py' is running"
if [[ $(ps -ef | grep src/main | grep -v grep) ]]; then
# if [[ $(ls -A) ]]; then
    echo "====> it is running!"
else
    echo "====> please run 'python3 validator.py' in a background shell!"
    exit 1
fi

# put in the good config
rm -rf response.zip
echo "====> fetching with specified 'config.yaml'"
curl -XPOST localhost:5000/generate -d ‘@$(pwd)/test/config.yaml’  -o response.zip
echo "====> extracting 'config.yaml' from the downloaded file"
unzip -d tempdir -o response.zip
diff -y tempdir/TennisGazelle-*/config.yaml test/config.yaml

exit 0