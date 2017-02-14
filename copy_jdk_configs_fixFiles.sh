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

# idea: there should be check that the directory we are coping from is valid jre (eg jre/bin/java exists) and not leftower, otherwise following may happen:
# <mvala> 1] install v1
# <mvala> 2] edit java.security
# <mvala> 3] remove v1
# <mvala> 4] install v2
# <mvala> 5] edit java.security
# <mvala> 6] install v1
# <mvala> 7] java.security is in original state instead of in state from step 5] (nor other "correct" as:
# <mvala> mno ten java.security je ale uplne puvodni, neni ani ve stavu po prvnim editu ani po druhym. cekal bych ze se bud obnovi z rpmsave nebo se prevede z v2

work rpmnew
work rpmorig

debug "Working with rpmorig (2)"
# simply moving old rpmsaves to new dir
# fix for config (replace) leftovers
files=`find $source | grep "\\.rpmorig$"`
  for file in $files ; do
    rpmsaveTarget=`echo $file | sed "s/$srcName/$targetName/"`
    debug "relocating $file to $rpmsaveTarget"
    mv $rma $file $rpmsaveTarget
  done
clean
