#!/bin/zsh
# All voicing in one go (run under the shared heavy-model lock): reference voices first, then scenarios one by one.
# After each scenario the marker out/<lang>/<id>/voice/.done tells the build lane it can start.
cd ${0:A:h}/../..
# VOICE_PY: a python with mlx-audio and mlx-whisper; can be set in .env.local (not in git)
[[ -f .env.local ]] && source .env.local
PY=${VOICE_PY:-python3}
while (( $(memory_pressure -Q | awk -F': ' '/percentage/ {print $2+0}') < 40 )); do sleep 10; done
python3 -c "
import json, os
for k, v in json.load(open('voices.local.json')).items():
    if v.get('source') and not os.path.exists(v['ref_audio']): print(v['source'], v['ref_audio'], v.get('lang', 'en'))
" | while read s d l; do $PY synth/tools/make_ref.py $s $d 10 $l; done
for key in $@; do
  if $PY synth/tools/voice.py $key; then touch out/$key/voice/.done && echo "[$key] voiced" >&3; else echo "[$key] voicing failed" >&3; fi
done
