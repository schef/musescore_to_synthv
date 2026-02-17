# MuseScore to SynthV converter
MuseScore to SynthV converter with Croatian-aware phoneme mapping, tempo support, and swing.

## Highlights
- Converts MuseScore 3 `.mscx` to Synthesizer V `.svp` (v153)
- Tempo changes, pickup bars, and swing (8th/16th)
- Croatian phoneme mapping and syllabic-R handling
- Per-voice export filters
- Supported MuseScore: 3.6.2 (MuseScore-3.6.2.548021370-x86_64.AppImage)

## Quickstart
`python mscx_to_svp.py examples/beach_boys-ballad_of_ole_betsy.mscx examples/beach_boys-ballad_of_ole_betsy.svp`

## Options
- `-d, --dict` Croatian phoneme dictionary mapping
- `-s, --shuffle` Swing percent (0-100)
- `-u, --shuffle-unit` Swing unit (`8` or `16`)
- `--voices` Comma-separated staff IDs or names (e.g. `1,3` or `Soprano,Tenor`)
- `-v, --verbose` Parser debug output

## Help
`python mscx_to_svp.py --help`

## Examples
Check out [Youtube](https://youtu.be/a3G_8BG2l7Q) or the `examples/` folder for project files and audio.
