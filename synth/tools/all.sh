#!/bin/zsh
# Voice and build scenarios in two lanes.
#   voicing (OmniVoice) - one pass under the shared heavy-model lock VOICE_LOCK (never two models at once),
#   scenarios one by one inside it (voice_lane.sh);
#   video build - its own queue BUILD_LOCK, as soon as a scenario's voice is ready.
# synth/tools/all.sh [<lang>/<id> ...]
cd ${0:A:h}/../..
# VOICE_PY: a python with mlx-audio and mlx-whisper; can be set in .env.local (not in git)
[[ -f .env.local ]] && source .env.local
PY=${VOICE_PY:-python3}
VOICE_LOCK=${VOICE_LOCK:-/tmp/dad-render.lock}
BUILD_LOCK=${BUILD_LOCK:-/tmp/vrp-build.lock}
LOGS=out/_logs
mkdir -p $LOGS
node_q() { node --experimental-strip-types --no-warnings -e "import('./scenarios/index.ts').then(m => console.log($1))"; }
# no arguments: every scenario in the languages of LANGS (default en; LANGS=en,ru for both)
keys=(${@:-$(node_q "m.SCENARIOS.filter(s => '${LANGS:-en}'.split(',').includes(s.lang)).map(m.keyOf).join(' ')")})
# key whose voice this scenario reuses (voiceFrom), or itself
src() { node_q "(s => s.lang + '/' + (s.voiceFrom ?? s.id))(m.byKey('$1'))"; }
mem='while (( $(memory_pressure -Q | awk -F": " "/percentage/ {print \$2+0}") < 40 )); do sleep 10; done'

for key in $keys; do rm -f out/$key/voice/.done; done

(
  need=()
  for key in $keys; do
    [[ $(src $key) == $key ]] || continue
    npm run -s lines $key >> $LOGS/voice.log 2>&1
    # everything already voiced with the same text - no lock needed
    if python3 -c "
import json, sys
lines = json.load(open('out/$key/lines.json'))
try: done = json.load(open('out/$key/voice/voice.json'))
except FileNotFoundError: sys.exit(1)
ok = lambda l: l['id'] in done and done[l['id']].get('text', l['text']) == l['text'] and done[l['id']].get('voice', l['voice']) == l['voice']
sys.exit(0 if all(ok(l) for l in lines) else 1)
"; then
      touch out/$key/voice/.done && echo "[$key] already voiced"
    else
      need+=($key)
    fi
  done
  (( ${#need} )) && lockf -k $VOICE_LOCK synth/tools/voice_lane.sh $need 3>&1 >> $LOGS/voice.log 2>&1
) &
voice=$!

for key in $keys; do
  s=$(src $key)
  while [[ ! -f out/$s/voice/.done ]] && kill -0 $voice 2>/dev/null; do sleep 5; done
  if [[ ! -f out/$s/voice/.done ]]; then echo "[$key] no voice, skipping"; continue; fi
  if lockf -k $BUILD_LOCK zsh -c "$mem; npm run -s build $key" >> $LOGS/build.log 2>&1; then
    echo "[$key] done: $PWD/out/$key.mp4"
  else
    echo "[$key] build failed, see $LOGS/build.log"
  fi
done
wait $voice
