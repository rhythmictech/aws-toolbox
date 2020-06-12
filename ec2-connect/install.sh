#!/bin/bash

# os detection
if [[ "$OSTYPE" == "linux-gnu"* ]]; then
        # linux, need to determine type
		echo "LINUX"
		# where will this live?
elif [[ "$OSTYPE" == "darwin"* ]]; then
        # Mac OSX
		echo "installing to /usr/local/bin"
		cp ec2-ez /usr/local/bin/
else
        # Unknown.
		echo "UNABLE"
fi
