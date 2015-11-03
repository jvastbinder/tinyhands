#/bin/bash

TOP="$(pwd)"

# source directories
DB_SRC="${TOP}/etc"
PHOTO_SRC="${TOP}/etc/interceptee_photos"
FORM_SRC="${TOP}/etc/scanned_forms"

if [ ! -f "${DB_SRC}/db.sqlite3.gz" ]
then
    echo "You must be at the top directory for tinyhands"
    exit 1
fi

# destination directories
PHOTO="${TOP}/media/interceptee_photos"
IRF_FORM="${TOP}/media/scanned_irf_forms"
VIF_FORM="${TOP}/media/scanned_vif_forms"

if [ -e "${TOP}/db.sqlite3" ]
then
    echo "There is already a database file at ${TOP}/db.sqlite3"
    echo "This script will not overwrite an existing database"
    echo "Please rename or remove the database before running this script"
    exit 2
fi

cp "${DB_SRC}/db.sqlite3.gz" "${TOP}"
cd "${TOP}"
gunzip db.sqlite3.gz

mkdir -p "${PHOTO}"
mkdir -p "${IRF_FORM}"
mkdir -p "${VIF_FORM}"

cd "${PHOTO_SRC}"
cp * "${PHOTO}"

cd "${FORM_SRC}"
cp * "${IRF_FORM}"
cp * "${VIF_FORM}"

