#!/bin/bash

#store the path given by the user
path=0;

#options
recursive=0;
ignore=0;

nbFile=0;
nbNorm=0;

while getopts ":ri" opt; do
  case $opt in
    r)
      #echo "-r was triggered!" >&2
	  recursive=1;
      ;;
    i)
	  #echo "-i was triggered!" >&2
	  ignore=1;
	  ;;
    \?)
      echo "Invalid option: -$OPTARG" >&2
      echo "Usage summary: [-r] [-i] path" >&2
      exit 1;
      ;;
  esac
done

path=${@:$#};


normalize_file () {
	filepath=$1;
	filename="${filepath##*/}";
	DIR=${filepath%/*};

	#if it's a file
	if [ -e $filepath ]; then
		#if recursive is enable and it's a directory readable
		if [ $recursive -eq 1 ] && [ -d $filepath ] && [ -r $filepath ]; then
			./my_normalizer.sh -r $filepath;
		# if it's not but it's still readable and not empty and it's not a file already normalized
		elif [ -r $filepath ] && [ -s $filepath ] && [[ $filename =~ ^[^norm_].*.wav$ ]]; then
			normname=norm_$filename;
			sox -v 0.80 --norm $filepath $DIR/$normname;
			((nbNorm++));
			echo $filename NORMALIZED -\> $normname;
			echo;
		elif [ $ignore -eq 1 ]; then
			echo $filename IGNORED;
			echo;
		fi
	fi
}

#if the path is wrong
if [ ! -e $path ]; then
	echo $path is not an existing file or directory;
	exit 1;
fi
#if the size is null
if [ ! -s $path ]; then
	echo $path is empty;
	exit 1;
fi
#if the destination is not readable
if [ ! -r $path ]; then
	echo $path is not readable;
	exit 1;
fi

#if it's an existing directory
if [ -d $path ]; then
	echo enter $path ...;
	#foreach file inside
	for file in $path/*; do
		((nbFile++))
		normalize_file $file;
	done
#if it's a file
else
	normalize_file $path
fi

#display number of files check + number of normalized files + total time
echo $path done: $nbFile checked, $nbNorm files normalized in $SECONDS s.

#Penser à ajouter une option pour effectuer le traitement récursivement sur les sous-dossiers