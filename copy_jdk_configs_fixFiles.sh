#!/bin/bash
config=$1
target=$2

debug="false"

#we should be pretty strict about removing once used (even "used" [with fail]) config file, as it may corrupt another installation
clean(){
  debug "cleanup: removing $config"
  rm -rf $config
}

debug(){
  if [ "x$debug" == "xtrue" ] ; then
    echo "$1"
  fi
}

if [ "x" == "x$config" ] ; then
  debug "no config file specified"
  exit 1
fi

if [ ! -f  "$config" ] ; then
  debug "$config file do not exists"
  # expected case, when no migration happened
  exit 0
fi 

if [ "x" == "x$target" ] ; then
  debug "no target dir specified"
  clean
  exit 2
fi

if [ ! -d  "$target" ] ; then
  debug "$target is not directory"
  clean
  exit 22
fi 

source=`cat $config` 

if [ "x" == "x$source" ] ; then
  debug "no information in $config"
  clean
  exit 3
fi

if [ ! -d  "$source" ] ; then
  debug "$source from $config is not directory"
  clean
  exit 33
fi 

debug "source: $source"

srcName=`basename $source`
targetName=`basename $target`

files=`find $target | grep "\\.rpmnew$"`
for file in $files ; do
  sf1=`echo $file | sed "s/\\.rpmnew$//"`
  sf2=`echo $sf1 | sed "s/$targetName/$srcName/"`
  # was file modified in origianl installation?
  rpm -Vf $source | grep -q $sf2
  if [ $? -gt 0 ] ; then
   debug "$sf2 was NOT modified, removing possibly corrupted $sf1 and renaming $file"
   rm $sf1 
   mv $file $sf1
   if [ $? -eq 0 ] ; then
     echo "restored $file to $sf1"
   else
     echo "FAILED to restore $file to $sf1"
   fi
  else
   debug "$sf2 was modified, keeping $file, and removing the duplicated original"
   # information is now backuped, in new directory anyway. Removing future rpmsave to allow rep -e
   rm $sf2
   # or its corresponding backup
   rm $sf2.rpmnew
  fi
done

clean
