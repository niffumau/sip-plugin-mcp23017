#!/bin/bash
# vim: ts=3 sw=3 sts=3 sr noet


print_notice() {
   echo -en "  \\e[1;34m${1}\\e[0m...\n"
}

if [[ $(id -u) -gt 0 ]]
then
    echo "run this command as root or sudo otherwise this script might fail"
    exit
fi


if [ "$#" -ne 1 ]; then

	SIPDIR="/home/niffum/SIP"

else
	SIPDIR="$1"
fi


# Check if the dir is actually there
if test -f "$SIPDIR/sip.py"; then
	echo "Installing plugin in $SIPDIR"
else
	print_notice "SIPDIR incorrect"
	exit
fi

print_notice "Updating files"

cp -u mcp23017.py $SIPDIR/plugins
cp -u mcp23017.html $SIPDIR/templates
cp -u mcp23017.js $SIPDIR/static/scripts
cp -u mcp23017-docs.html $SIPDIR/static/docs/plugins
cp -u mcp23017.manifest $SIPDIR/plugins/manifests


print_notice "Updating files"
chmod +x $SIPDIR/plugins/*.py

print_notice "Clearing cache"
rm $SIPDIR/__pycache__/*
rm $SIPDIR/plugins/__pycache__/*

print_notice "Installation of plugin done"

