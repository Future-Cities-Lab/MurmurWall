#!/bin/bash


while [ "true" ]
do 
	if [ "$(pgrep "python")" ]
	then
	    echo "It's on"
	else
	    echo "It's off, shutting down"    
	    sudo reboot
	fi
	sleep 1
done


