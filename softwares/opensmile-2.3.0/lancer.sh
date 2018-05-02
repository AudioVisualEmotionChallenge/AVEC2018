#!/bin/bash
echo "Bienvenue dans le smile extract, assistant d'extraction OpenSmile :"
ls *.conf ./config/
echo "Choisissez votre fichier de configuration sans mettre l'extension (dans /config) :"
read fichierconf
ls *.wav ../recordings_audio/
echo "Choisissez votre fichier audio sans mettre l'extension (dans /../recordings_audio) :"
read audio
echo "Choisissez votre csv output sans l'extension (sera placé dans le dossier courant) :"
read fsortie
inst/bin/SMILExtract -C config/$fichierconf.conf -I ../recordings_audio/$audio.wav -O $fsortie.csv
