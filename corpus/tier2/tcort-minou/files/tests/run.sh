#!/bin/sh

IN=${INDIR}/${1}.lol
OUT=${OUTDIR}/${1}.out
EX=${EXDIR}/${1}.ex

${MINOU} ${IN} > ${OUT}
RESULT=$?
if [ $RESULT -gt 0 ]
then
	exit 1
fi

if [ -f ${EX} ]
then
	diff -u ${EX} ${OUT} > /dev/null
	RESULT=$?
	if [ $RESULT -gt 0 ]
	then
		exit 1
	fi
fi

exit 0
