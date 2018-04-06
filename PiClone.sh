#!/bin/bash

#Author Jalen Shell.
#This small script is to make a helpful way for a user to clone a system and restore it. Sudo permissions will be needed so it should be fine if you "sudo ./{This Program}".
#Date Modified: 4/5/2018
#Any questions can be emailed to jalenshell11@gmail.com about this script.
#Website used to help create this script: https://wiki.archlinux.org/index.php/disk_cloning

function runDD()
{
		echo "Enter path you want to copy (Source):"
		read src
		echo "Enter path you want paste (Destination):"
		read dest
		
		echo "Is this a partion clone (y/n)?	(If no, then it will be a full disk clone) "
		read decision
		
		if ($decision -eq "y"); 
		then
			sudo dd if=$src of=$dest bs=64K conv=noerror,sync status=progress
		else 
			sudo dd if=$src of=$dest bs=64K conv=noerror,sync status=progress
}

function runDI()
{
	echo "Creating Image"
	echo "Enter the path you want to get an image of: (Or the location of where to put the data back when restoring)"
	read src
	echo "Enter path you want to backup/save the image: (Or the backup location if restoring)"
	read dest
	
	echo "Is this an image creation (y/n)?	(If no, then it will be a restore) "
	read decision
	
	if ($decision -eq "y"); 
	then	
		#Backup the drive
		sudo dd if=$src conv=sync,noerror bs=64K | gzip -c > $dest.img.gz
	
		#More data about the drive is made
		sudo fdisk -l $src > $dest/List__fdisk.info
	
	elif($decision -eq "n":
	then	
		gunzip -c $dest.img.gz | dd of=$src
	
}

echo "Reminder: sudo needed."
echo
echo "What Cloner do you want to use?"
echo "1. dd"
echo "2. partimage(More Visual Friendly)"
echo "3. Create a disk image or Restore"

#Get user input for this variable
read choice

if ($choice -eq 1); 
then
	echo "WARNING!!  Always ensure that the destination drive or partition is of equal or greater size than the source..."
	# Check if dd is installed.
	if command -v dd 2>/dev/null; 
	then
		runDD
	else
		sudo apt-get -y install dd
		runDD
		
	fi
	echo "Done!!"
elif ($choice -eq 2); 
then
	# Check if partimage is installed.
	if command -v partimage 2>/dev/null; 
	then
		sudo partimage
	else
		sudo apt-get -y install partimage
		sudo partimage
	fi
		echo "Done!!"
elif ($choice -eq 3):
then
	# Check if dd and gzip is installed
	if command -v dd 2>/dev/null; 
	then
		sudo apt-get -y install dd
	fi
	if command -v gzip 2>/dev/null;
	then
		sudo apt-get -y install gzip
	fi
	if command -v fdisk 2>/dev/null; 
	then
		sudo apt-get -y install fdisk
	fi
	runDI
	echo "Done!!"
fi

