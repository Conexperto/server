#!/bin/sh

# Decrypt the file
gpg --quiet --batch --yes --decrypt --passphrase="$SECRET_PASSPHRASE" \
--output $OUTPUT $INPUT
