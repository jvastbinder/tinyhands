#!/bin/bash

set -x

## rsync select files from the THI production server.

## Notes on rsync flags
## --delete (delete extraneous files on receiving side) -- DON'T DO THIS
## --archive == -rlptgoD
##  --recursive (recurse into directories)
##  --links     (copy symlinks as symlinks)
##  --perms     (preserve permissions)
##  --times     (preserve modification times)
##  --group     (preserve group)
##  --owner     (preserve owner)
##  --devices   (-D => preserve device files - SU only)
##  --specials  (-D => preserve special files)

RS='mkdir --parents'
YEAR=$(date '+%Y')
MONTH=$(date '+%B')
NEW_DIR=backups/$YEAR/$MONTH

RSYNC='rsync --verbose --archive --progress --rsh=ssh'

THI_PROD='thi-production:/home/dreamsuite/tinyhands'

BACKUP_DIR='/home/thi/tinyhands/bin/backups'

NOW=$(date '+%F-%H-%M')

$RSYNC $THI_PROD/db.sqlite3 $BACKUP_DIR/db-$NOW.sqlite3
$RSYNC $THI_PROD/media .
