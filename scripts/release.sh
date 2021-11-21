#!/bin/sh

# Decrypt for SDK website
gpg --quiet --batch --yes --decrypt --passphrase="$SECRET_PASSPHRASE" \
	--output "./src/config/$FIREBASE_WEB_SDK_FILE.1" "./src/config/$FIREBASE_WEB_SDK_FILE.gpg"

# Decrypt for SDK admin
gpg --quiet --batch --yes --decrypt --passphrase="$SECRET_PASSPHRASE" \
 --output "./src/config/$FIREBASE_ADMIN_SDK_FILE.1" "./src/config/$FIREBASE_ADMIN_SDK_FILE.gpg"
