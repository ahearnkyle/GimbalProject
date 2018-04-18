#!/bin/bash

#Author Jalen Shell.
#This small script is to make a helpful way for a user to clone a system and restore it. Sudo permissions will be needed so it should be fine if you "sudo ./{This Program}".
#Date Modified: 4/18/2018
#Any questions can be emailed to jalenshell11@gmail.com about this script.
#Website used to help create this script: https://wiki.archlinux.org/index.php/disk_cloning

## Begin Functions.
function runDD()
{
		echo 
		read -p "Enter path you want to copy (Source): " src
		echo 
		read -p "Enter path you want to paste (Destination): " dest
		
		echo 
		read -p "Is this a partition clone (y/n)?	(If no, then it will be a full disk clone) " decision
		
		if [ $decision = "y" ]; 
		then
			sudo dd if=$src of=$dest bs=64K conv=noerror,sync status=progress
		else 
			sudo dd if=$src of=$dest bs=64K conv=noerror,sync status=progress
}

# This function used to run the dd and fdisk and gzip programs to create an image and restore an image.
function runDI()
{
	echo "Is this an image creation (y/n)?	(If no, then it will be a restore) "
	read decision
	
	echo "Enter the path you want to get an image of: (Or the location of where to put the data back when restoring)"
	read src
	echo "Enter path you want to backup/save the image: (Or the backup location if restoring)"
	read dest
	
	if [ $decision = "y" ]; 
	then	
		#Backup the drive
		sudo dd if=$src conv=sync,noerror bs=64K | gzip -c > $dest.img.gz
	
		#More data about the drive is made
		sudo fdisk -l $src > $dest/List__fdisk.info
		
	elif [ $decision = "n" ]:
	then	
		gunzip -c $dest.img.gz | dd of=$src
	
}
## End Functions.

## MAIN
echo "Reminder: sudo ./{This script} is needed."
echo
echo "What Cloner/ do you want to use?"
echo "1. dd"
echo "2. partimage(More Visual Friendly)"
echo "3. Create a disk image or Restore (Uses dd and fdisk)"

#Get user input for this variable
read  -p "Choice: " choice

if [ $choice = 1 ]; 
then
	echo "WARNING!!  Always ensure that the destination drive or partition is of equal or greater size than the source..."
	# Check if dd is installed.
	if command -v dd >/dev/null; 
	then
		runDD
	else
		sudo apt-get -y install dd
		runDD
		
	fi
	echo "Done!!"
elif [ $choice = 2 ]; 
then
	# Check if partimage is installed.
	if command -v partimage >/dev/null; 
	then
		sudo partimage
	else
		sudo apt-get -y install partimage
		sudo partimage
	fi
		echo "Done!!"
elif [ $choice = 3 ]:
then
	if command -v dd >/dev/null; 
	then
		sudo apt-get -y install dd
	fi
	# Check if dd and gzip is installed
	if command -v gzip >/dev/null;
	then
		sudo apt-get -y install gzip
	fi
	if command -v fdisk >/dev/null; 
	then
		sudo apt-get -y install fdisk
	fi
	runDI
	echo "Done!!"
fi

