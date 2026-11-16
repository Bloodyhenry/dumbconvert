#!/bin/sh
# Starts DumbConvert inside the Flatpak: the app and NegPy live in /app/share/dumbconvert
export PYTHONPATH=/app/share/dumbconvert:/app/share/dumbconvert/vendor/negpy
exec /app/bin/python3.14 -m simpleneg "$@"
