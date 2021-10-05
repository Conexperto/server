#!/bin/sh

AUTH_HOST="0.0.0.0"
AUTH_PORT="9098"
UI_ENABLED="false"
UI_HOST="0.0.0.0"
UI_PORT="9001"
FIREBASE_PROJECT="conexperto-6b5e7"


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
