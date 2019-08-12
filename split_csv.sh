#!/bin/bash
################################################################################################
# split_csv.sh
# Delimiter and Columns to extract Mails(lowercase)/Pws
################################################################################################

# Config
NEWDELIM="║"
USAGE="USAGE: $0 -f FILE "
F_FLAG=0

############## FUNCTIONS
# remove blank lines param $1=file
remove_blank () { 
  echo -n "Removing blank lines from ${1} ..."
  sed -i -r '/^\s*$/d' ${1}
  if [ $? -ne 0 ]; then
    echo "ERROR: sed failed!"
    exit 1
  fi
  echo "DONE"
}

# sort -u file, param $1=file
sort_uniq () {
  echo -n "Sorting..."
  sort -T /data/JULIAN/tmp/ -u ${1} -o ${1}_su
  if [ $? -ne 0 ]; then
      echo "ERROR: sort -u failed!"
      exit 1
  fi
  mv ${1}_su ${1}
  echo "DONE"
}

############## END FUNCTIONS


# Get and check arguments
while getopts f: opt; do
  case "${opt}" in
    f )
      FILE=$OPTARG
      F_FLAG=1
      ;;
    \? )
      echo ${USAGE} 
      exit 1
      ;;
  esac
done

if [ ${F_FLAG} -eq 0 ]
  then
  echo "ERROR: Please specify all arguments!"  
  echo ${USAGE}
  exit 1
fi

if [ ! -f ${FILE} ]
  then
  echo "ERROR: ${FILE} not a file"
  echo ${USAGE}
  exit 1
fi

# Extract file, path and number
DIR=`dirname ${FILE}`
FNAME=`basename ${FILE}`
FSHORTNAME=${FNAME%.*}
FNUM=`echo ${FNAME} | cut -d'_' -f 1`

# Generate file names
WORKFILE=${FILE}.tmp
FEP=${DIR}/${FSHORTNAME}_emails_passwords.txt
FO=${DIR}/${FSHORTNAME}_originalfields.txt

# Check and create lock file
if [ -a ${FILE}.lock ]
then
  echo "ERROR: ${FILE} already in use or old lockfile still there. Check for running process and/or delete lock file."
  exit 1
fi
touch ${FILE}.lock

# ask for stuff
{
IFS=''
while [ -z ${DELIM} ] || [ -z ${EMAILCOLUMN} ] || [ -z ${PWCOLUMN} ] || [ ! ${RESULT}=="y" ]
do
  echo "Check the first 30 lines of ${FILE}:"
  head -30 ${FILE}
  read -p "File usable? [y/n]" USABLE
  if [ ${USABLE}=="n" ]
  then
    mv -v ${FILE} ${FILE}.SPECIAL
    echo "RENAMED file to special!"
    rm ${FILE}.lock
    exit 0
  fi
  read -p "Enter the delimiter: " DELIM
  read -p "Enter the e-mail column(columns start at 1): " EMAILCOLUMN
  read -p "Enter the password column(columns start at 1): " PWCOLUMN
  read -p "Delimiter is '${DELIM}' e-mail column is ${EMAILCOLUMN} and password column is ${PWCOLUMN}, is that correct? [y/n] " RESULT
done
}

# Check and create work file
if [ -a ${WORKFILE} ]
then
  echo "ERROR: ${WORKFILE} already in use or old workfile still there. Check for running process and/or delete work file."
  exit 1
fi
echo -n "Creating workfile..."
cp -v ${FILE} ${WORKFILE}
echo "DONE"

# Update vars
EMAILCOLUMN=\$${EMAILCOLUMN}
PWCOLUMN=\$${PWCOLUMN}

# Remove blank lines
remove_blank ${WORKFILE}

# Sort uniq the file
sort_uniq ${WORKFILE}

# Reformat and save in different files
echo -n "Reformatting..."
AWK="awk -v FS='${DELIM}' -v OFS='${NEWDELIM}' '{ ${EMAILCOLUMN}=tolower(${EMAILCOLUMN}); print > \"${FO}\"; emailcheck = match(${EMAILCOLUMN}, /[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,6}/); if (emailcheck) { print ${EMAILCOLUMN},${PWCOLUMN} > \"${FEP}\" } }' ${WORKFILE}"
eval ${AWK}
if [ $? -ne 0 ]; then
    echo "ERROR: awk failed!"
    exit 1
fi
echo "DONE"

# Sort uniq the email,password file
sort_uniq ${FEP}

# Sort uniq the originals file
sort_uniq ${FO}

# Clean up
echo -n "Cleaning up..."

# RENAME/MOVE TO PROCESSED
PDIR=`echo "${DIR}" | sed "s/NEW-INDEX/PROCESSED-INDEX/"`
mv -v ${FILE} ${FILE}.DONE
mv -v ${FILE}.DONE ${PDIR}
mv -v ${FO} ${PDIR}

DATE=`date +%Y%m%d`
IMPORTDIR=/data/JULIAN/PROCESSED-INDEX/import/${DATE}/
mkdir -p ${IMPORTDIR}
mv -v ${FEP} ${IMPORTDIR}


# Remove working files and lock
rm ${FILE}.lock
rm ${WORKFILE}
echo "DONE"
