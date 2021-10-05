#!/bin/sh

AUTH_HOST="0.0.0.0"
AUTH_PORT="9099"
UI_ENABLED="false"
UI_HOST="0.0.0.0"
UI_PORT="9000"
FIREBASE_PROJECT="conexperto-admin"


cat << EOF > ./firebase.json
{
	"emulators": {
		"auth": {
			"host": "$AUTH_HOST",
			"port": $AUTH_PORT
		},
		"ui": {
			"enabled": $UI_ENABLED,
			"host": "$UI_HOST",
			"port": $UI_PORT
		}
	}
}
EOF

cat << EOF > ./.firebaserc
{
	"projects": {
		"default": "$FIREBASE_PROJECT"
	}
}
EOF


firebase emulators:start
