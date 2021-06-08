#!/bin/bash

# Is Server running?

echo "====> Validating that `validator.py` is running"
if ; then
    echo "====> it is running!"
else
    echo "====> please run `python3 validator.py` in a background shell!"
    exit 1
fi

exit 0