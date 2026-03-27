#!/bin/bash
if [[ $(id -u) -gt 0 ]]
then
    echo "run this command as root or sudo otherwise this script might fail"
    exit
fi

if [ "$#" -ne 1 ]; then

  while true; do
    read -p "Enter full path of your SIP installation without trailing slash: " SIPDIR

        if [[ $SIPDIR = "q" ]] || [[ $SIPDIR = "Q" ]] 
        then 
            exit 999
        fi
        if test -f "$SIPDIR/sip.py"; then
            echo "Installing plugin in $SIPDIR"
            break
        fi
        echo "$SIPDIR not found, please try again"
  done

  else
    SIPDIR="$1"
fi

cp -u *.html $SIPDIR/templates
cp -u *.py $SIPDIR/plugins
cp -u *.manifest $SIPDIR/plugins/manifests
chmod +x $SIPDIR/plugins/*.py
echo 'Installation of plugin done'
