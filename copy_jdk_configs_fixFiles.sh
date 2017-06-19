#!/bin/bash
config=$1
target=$2

debug="false"

rma=""
  if [ "x$debug" == "xtrue" ] ; then
    rma="-v"
  fi

debug(){
  if [ "x$debug" == "xtrue" ] ; then
    echo "$1"
  fi
}

#we should be pretty strict about removing once used (even "used" [with fail]) config file, as it may corrupt another installation
clean(){
  debug "cleanup: removing $config"
  rm -rf $config
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
debug "target: $target"

work(){
  if [ "X$1" == "Xrpmnew" -o "X$1" == "Xrpmorig" ] ; then
    debug "Working with $1 (1)"
  else
    debug "unknown parameter: $1"
    return 1
  fi

  local files=`find $target | grep "\\.$1$"`
  for file in $files ; do
    local sf1=`echo $file | sed "s/\\.$1$//"`
    local sf2=`echo $sf1 | sed "s/$targetName/$srcName/"`
    # was file modified in origianl installation?
    rpm -Vf $source | grep -q $sf2
    if [ $? -gt 0 ] ; then
     if [ "X$1" == "Xrpmnew" ] ; then
       debug "$sf2 was NOT modified, removing possibly corrupted $sf1 and renaming from $file"
       rm $rma $sf1 
       mv $rma $file $sf1
       if [ $? -eq 0 ] ; then
         echo "restored $file to $sf1"
       else
         echo "FAILED to restore $file to $sf1"
       fi
    fi
     if [ "X$1" == "Xrpmorig" ] ; then
       debug "$sf2 was NOT modified, removing possibly corrupted $file"
       rm $rma $file
    fi
    else
     debug "$sf2 was modified, keeping $file, and removing the duplicated original"
     # information is now backuped, in new directory anyway. Removing future rpmsave to allow rpm -e
     rm -f $rma $sf2
     # or its corresponding backup
     rm -f $rma $sf2.$1
    fi
done
}


srcName=`basename $source`
targetName=`basename $target`

work rpmnew
work rpmorig

debug "Working with rpmorig (2)"
# simply moving old rpmsaves to new dir
# fix for config (replace) leftovers
files=`find $source | grep "\\.rpmorig$"`
  for file in $files ; do
    rpmsaveTarget=`echo $file | sed "s/$srcName/$targetName/"`
    debug "relocating $file to $rpmsaveTarget"
    if [ -e $rpmsaveTarget ] ; then
      rm $rma $file
    else
      mv $rma $file $rpmsaveTarget
    fi
  done

debug "Working with rpmsave (1)"
files=`find $source | grep "\\.rpmsave$"`
  for file in $files ; do
    rpmsaveTarget=`echo $file | sed "s/$srcName/$targetName/"`
    debug "relocating $file to $rpmsaveTarget"
    if [ -e $rpmsaveTarget ] ; then
      rm $rma $file
    else
      mv $rma $file $rpmsaveTarget
    fi
  done


#warning: file /usr/lib/jvm/java-1.8.0-openjdk-1.8.0.131-11.b12.el7.x86_64-debug/jre/lib/applet: remove failed: No such file or directory
#warning: file /usr/lib/jvm/java-1.8.0-openjdk-1.8.0.131-11.b12.el7.x86_64-debug/jre/lib/amd64/client: remove failed: No such file or directory
#those dirs might be mepty by installtion, filling to not be rmeoved later
blackdirs="$source/jre/lib/applet $source/jre/lib/*/client"
for blackdir in $blackdirs; do
  if [ -e $blackdir ] ; then
    debug "nasty $blackdir  exists, filling"
    touch $blackdir/C-J-C_placeholder
  else
    debug "nasty $blackdir  DONT exists, ignoring"
  fi
done

debug "cleaning legacy leftowers"
if [ "x$debug" == "xtrue" ] ; then
  find $source -empty -type d -delete
  rmdir $rma $source
else
  find $source -empty -type d -delete 2>/dev/null >/dev/null
  rmdir $rma $source 2>/dev/null >/dev/null
fi

# and remove placeholders
for blackdir in $blackdirs; do
  if [ -e $blackdir ] ; then
    debug "nasty $blackdir  exists, cleaning placeholder"
    rm $blackdir/C-J-C_placeholder
  else
    debug "nasty $blackdir  DONT exists, ignoring again"
  fi
done

clean
