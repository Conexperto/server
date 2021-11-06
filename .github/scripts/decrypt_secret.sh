#!/bin/sh

# Decrypt the file
gpg --quiet --batch --yes --decrypt --passphrase="$SECRET_PASSPHRASE" \
--output ./src/config/conexperto-6b5e7-sdk.json ./src/config/conexperto-6b5e7-sdk.json.gpg

gpg --quiet --batch --yes --decrypt --passphrase="$SECRET_PASSPHRASE" \
--output ./src/config/conexperto-admin-sdk.json ./src/config/conexperto-admin-sdk.json.gpg
