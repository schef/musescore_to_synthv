#!/usr/bin/env python

import click
import json
import re
import uuid
import musescore_parser as MP
import jp_to_hr

ONE_BEAT = 705600000
TAB = "  "

time_signature_n = 0
time_signature_d = 0
pitch = 0
duration = 0
onset = 0
lyric = ""
last_lyric = ""
comment = ""
tie = False
dot = 0
staff_num = 0
tuplet = False

use_hr_dict = False
tempo_events = []
shuffle_percent = 0.0
shuffle_unit = 8
current_notes = []
tracks_data = []
staff_names = {}
current_staff_id = None
pickup_offset = 0
pending_pickup_len = None


def get_time_signature_duration(n, d):
    # print("get_time_signature_duration")
    if n == 4 and d == 4:
        return int(ONE_BEAT * 4)
    elif n == 3 and d == 4:
        return int(ONE_BEAT * 3)
    elif n == 6 and d == 8:
        return int(6 * int(ONE_BEAT / 2))


def get_measure_length(length_value):
    if not length_value:
        return None
    if "/" not in length_value:
        return None
    try:
        numerator, denominator = length_value.split("/", 1)
        numerator = int(numerator.strip())
        denominator = int(denominator.strip())
    except ValueError:
        return None
    if denominator == 0:
        return None
    whole_note = int(ONE_BEAT * 4)
    return int(whole_note * numerator / denominator)


duration_type = {
    "measure": None,
    "whole": int(ONE_BEAT * 4),
    "half": int(ONE_BEAT * 2),
    "quarter": int(ONE_BEAT),
    "eighth": int(ONE_BEAT / 2),
    "16th": int(ONE_BEAT / 4),
    "32nd": int(ONE_BEAT / 8),
}


def generate_lyric(l):
    if l in ["-", "", "", None]:
        return "-"
    global use_hr_dict
    if use_hr_dict:
        tokens = map_hr_text_to_tokens(l)
        if not tokens:
            return "-"
        return "." + " ".join(tokens)
    return re.sub(r"\W+", "", l)


def map_hr_text_to_tokens(text):
    if not text:
        return []
    text = text.lower()
    tokens = []
    index = 0
    while index < len(text):
        digraph = text[index : index + 2]
        if digraph in jp_to_hr.jp_to_hr:
            mapped = jp_to_hr.jp_to_hr.get(digraph)
            index += 2
        else:
            mapped = jp_to_hr.jp_to_hr.get(text[index])
            index += 1
        if not mapped:
            continue
        tokens.extend(mapped.split())
    return tokens


def apply_syllabic_r(phoneme_string):
    if not phoneme_string:
        return phoneme_string
    tokens = phoneme_string.split()
    if not tokens:
        return phoneme_string
    vowel_tokens = {
        "aa",
        "ae",
        "ah",
        "ao",
        "aw",
        "ay",
        "eh",
        "er",
        "ey",
        "ih",
        "iy",
        "ow",
        "oy",
        "uh",
        "uw",
        "ax",
    }
    updated = []
    for idx, token in enumerate(tokens):
        if token == "r":
            prev_token = tokens[idx - 1] if idx > 0 else None
            next_token = tokens[idx + 1] if idx < len(tokens) - 1 else None
            prev_vowel = prev_token in vowel_tokens if prev_token else False
            next_vowel = next_token in vowel_tokens if next_token else False
            if not prev_vowel and not next_vowel:
                updated.append("ax")
                updated.append("r")
                continue
        updated.append(token)
    return " ".join(updated)


def generate_phonemes(l):
    if l in ["-", "", "", None]:
        return "-"
    global use_hr_dict
    if use_hr_dict:
        tokens = map_hr_text_to_tokens(l)
        if not tokens:
            return "-"
        return apply_syllabic_r(" ".join(tokens))
    return apply_syllabic_r(re.sub(r"\W+", " ", l).strip())


def format_bpm(bpm):
    value = "{:.3f}".format(bpm).rstrip("0").rstrip(".")
    if "." not in value:
        value += ".0"
    return value


def generate_project_start(tempo_list):
    tempo_output = tempo_list[:]
    if not tempo_output:
        tempo_output = [(0, 90.0)]
    elif tempo_output[0][0] != 0:
        tempo_output = [(0, tempo_output[0][1])] + tempo_output
    string = ""
    string += "{" + "\n"
    string += '    "version": 7,' + "\n"
    string += '    "meter": [' + "\n"
    string += "        {" + "\n"
    string += '            "measure": 0,' + "\n"
    string += '            "beatPerMeasure": 4,' + "\n"
    string += '            "beatGranularity": 4' + "\n"
    string += "        }" + "\n"
    string += "    ]," + "\n"
    string += '    "tempo": [' + "\n"
    for index, (position, bpm) in enumerate(tempo_output):
        string += "        {" + "\n"
        string += '            "position": ' + str(position) + "," + "\n"
        string += '            "beatPerMinute": ' + format_bpm(bpm) + "\n"
        string += "        }"
        if index < len(tempo_output) - 1:
            string += ","
        string += "\n"
    string += "    ]," + "\n"
    string += '    "tracks": [' + "\n"
    return string


def generate_staff_start():
    global staff_num
    string = ""
    string += "        {" + "\n"
    string += '            "name": "Unnamed Track",' + "\n"
    string += '            "dbName": "Eleanor Forte",' + "\n"
    string += '            "color": "15e879",' + "\n"
    string += '            "displayOrder": ' + str(staff_num) + "," + "\n"
    string += '            "dbDefaults": {},' + "\n"
    string += '            "notes": [' + "\n"
    return string


def build_note_data(onset_value, duration_value, lyric_value, pitch_value):
    phonemes = generate_phonemes(lyric_value)
    return {
        "musicalType": "singing",
        "onset": onset_value,
        "duration": duration_value,
        "lyrics": "-" if lyric_value in [None, ""] else lyric_value,
        "phonemes": phonemes,
        "accent": "",
        "pitch": pitch_value,
        "detune": 0,
        "instantMode": False,
        "attributes": {
            "dF0Vbr": 0.0,
            "dF0Jitter": 0.0,
            "evenSyllableDuration": False,
        },
        "systemAttributes": {
            "evenSyllableDuration": True,
        },
        "pitchTakes": {
            "activeTakeId": 0,
            "takes": [
                {
                    "id": 0,
                    "expr": 0.0,
                    "liked": False,
                }
            ],
        },
        "timbreTakes": {
            "activeTakeId": 0,
            "takes": [
                {
                    "id": 0,
                    "expr": 0.0,
                    "liked": False,
                }
            ],
        },
    }


def get_shuffle_offset(onset_value):
    if shuffle_percent <= 0.0:
        return 0
    onset_int = int(round(onset_value))
    if abs(onset_value - onset_int) > 0.0001:
        return 0
    if shuffle_unit == 16:
        subdivision = int(ONE_BEAT / 4)
    else:
        subdivision = int(ONE_BEAT / 2)
    if subdivision <= 0:
        return 0
    if onset_int % subdivision != 0:
        return 0
    if (onset_int // subdivision) % 2 != 1:
        return 0
    return int(subdivision * shuffle_percent / 100.0)


def build_default_parameters():
    return {
        "pitchDelta": {"mode": "linear", "points": [0, 0.0]},
        "vibratoEnv": {"mode": "linear", "points": [0, 1.0]},
        "loudness": {"mode": "linear", "points": [0, 0.0]},
        "tension": {"mode": "linear", "points": [0, 0.0]},
        "breathiness": {"mode": "linear", "points": [0, 0.0]},
        "voicing": {"mode": "linear", "points": [0, 1.0]},
        "gender": {"mode": "linear", "points": [0, 0.0]},
        "toneShift": {"mode": "cubic", "points": []},
    }


def build_main_ref():
    return {
        "groupID": str(uuid.uuid4()),
        "blickAbsoluteBegin": 0,
        "blickAbsoluteEnd": -1,
        "blickOffset": 0,
        "pitchOffset": 0,
        "isInstrumental": False,
        "systemPitchDelta": {"mode": "cubic", "points": []},
        "database": {
            "name": "Mo Chen",
            "language": "mandarin",
            "phoneset": "xsampa",
            "languageOverride": "english",
            "phonesetOverride": "arpabet",
            "backendType": "SVR2AI",
            "version": "109",
        },
        "dictionary": "",
        "voice": {
            "vocalModeInherited": True,
            "vocalModePreset": "",
            "vocalModeParams": {},
        },
        "pitchTakes": {
            "activeTakeId": 0,
            "takes": [
                {
                    "id": 0,
                    "expr": 0.0,
                    "liked": False,
                }
            ],
        },
        "timbreTakes": {
            "activeTakeId": 0,
            "takes": [
                {
                    "id": 0,
                    "expr": 0.0,
                    "liked": False,
                }
            ],
        },
    }


def build_track_data(notes, display_order, track_name):
    return {
        "name": track_name,
        "dispColor": "ff15e879",
        "dispOrder": display_order,
        "renderEnabled": False,
        "mixer": {
            "gainDecibel": 0.0,
            "pan": 0.0,
            "mute": False,
            "solo": False,
            "display": True,
        },
        "mainGroup": {
            "name": "main",
            "uuid": "main",
            "parameters": build_default_parameters(),
            "vocalModes": {},
            "notes": notes,
        },
        "mainRef": build_main_ref(),
        "groups": [],
    }


def build_project_data(tracks):
    numerator = time_signature_n or 4
    denominator = time_signature_d or 4
    tempo_output = tempo_events[:]
    if not tempo_output:
        tempo_output = [(0, 90.0)]
    elif tempo_output[0][0] != 0:
        tempo_output = [(0, tempo_output[0][1])] + tempo_output
    tempo_output = sorted(tempo_output, key=lambda item: item[0])
    return {
        "version": 153,
        "time": {
            "meter": [
                {
                    "index": 0,
                    "numerator": numerator,
                    "denominator": denominator,
                }
            ],
            "tempo": [
                {"position": position, "bpm": bpm} for position, bpm in tempo_output
            ],
        },
        "library": [],
        "tracks": tracks,
        "renderConfig": {
            "destination": "",
            "filename": "untitled",
            "numChannels": 1,
            "aspirationFormat": "noAspiration",
            "bitDepth": 16,
            "sampleRate": 44100,
            "exportMixDown": True,
            "exportPitch": False,
        },
    }


def set_staff_start(staff_id):
    global onset
    global current_notes
    global current_staff_id
    global pickup_offset
    global pending_pickup_len
    onset = 0
    # print(generate_staff_start())
    current_notes = []
    current_staff_id = staff_id
    pickup_offset = 0
    pending_pickup_len = None


def set_staff_end():
    # print(generate_staff_end())
    global tracks_data
    global staff_num
    name = staff_names.get(current_staff_id, "Unnamed Track")
    tracks_data.append(build_track_data(current_notes, staff_num, name))
    staff_num += 1


def apply_pickup_offset(pickup_len):
    global pickup_offset
    if pickup_len is None:
        return
    if duration_type["measure"] is None:
        return
    offset = duration_type["measure"] - pickup_len
    if offset > 0:
        pickup_offset = offset


def set_measure_len(length_value, measure_index):
    global pending_pickup_len
    if measure_index != 0:
        return
    pickup_len = get_measure_length(length_value)
    if pickup_len is None:
        return
    if duration_type["measure"] is None:
        pending_pickup_len = pickup_len
        return
    apply_pickup_offset(pickup_len)


def set_staff_name(staff_id, name):
    if not staff_id:
        return
    if not name:
        return
    staff_names[staff_id] = name


def set_time_signature(n, d):
    global time_signature_n
    time_signature_n = int(n)
    global time_signature_d
    time_signature_d = int(d)
    global duration_type
    duration_type["measure"] = get_time_signature_duration(
        time_signature_n, time_signature_d
    )
    global pending_pickup_len
    if pending_pickup_len:
        apply_pickup_offset(pending_pickup_len)
        pending_pickup_len = None


def set_pitch(p, d):
    global pitch
    global duration
    global output_string
    global onset
    global lyric
    global tie
    global dot
    global current_notes
    global pickup_offset

    pitch = int(p)
    duration += duration_type[d]

    if dot > 0:
        duration += int(duration_type[d] / 2)
    if dot > 1:
        duration += int(duration_type[d] / 4)
    if dot > 2:
        duration += int(duration_type[d] / 8)
    dot = 0

    if tuplet:
        duration = duration * 2 / 3

    if tie:
        tie = False
    else:
        if lyric == "":
            lyric = "-"
        # print(generate_note())
        base_onset = onset + pickup_offset
        shuffle_offset = get_shuffle_offset(base_onset)
        output_onset = base_onset
        output_duration = duration
        if shuffle_offset > 0:
            output_onset = base_onset + shuffle_offset
            output_duration = max(0, duration - shuffle_offset)
            if current_notes:
                last_note = current_notes[-1]
                if last_note["onset"] + last_note["duration"] == base_onset:
                    last_note["duration"] += shuffle_offset
        current_notes.append(
            build_note_data(output_onset, output_duration, lyric, pitch)
        )
        onset += duration
        duration = 0
        lyric = ""


def set_rest(d):
    global onset
    global dot

    duration = duration_type[d]

    if dot > 0:
        duration += int(duration_type[d] / 2)
    if dot > 1:
        duration += int(duration_type[d] / 4)
    if dot > 2:
        duration += int(duration_type[d] / 8)
    dot = 0

    if tuplet:
        duration = duration * 2 / 3

    onset += duration


def set_lyric(l):
    global lyric
    global last_lyric
    lyric = l
    last_lyric = l


def set_tie():
    global tie
    tie = True


def set_dot(num):
    global dot
    dot = int(num)


def set_tuplet(status):
    global tuplet
    if status:
        tuplet = True
    else:
        tuplet = False


def set_tempo(tempo):
    if tempo in [None, "", "-"]:
        return
    try:
        bpm = float(tempo) * 60.0
    except ValueError:
        return
    global tempo_events
    position = onset
    if onset > 0:
        position = onset + pickup_offset
    tempo_events.append((position, bpm))


def write_to_file(file_name, data):
    with open(file_name, "w") as write_file:
        write_file.write(data)


@click.command()
@click.argument("readfile", type=click.Path(exists=True))
@click.argument("writefile", type=click.Path(exists=False))
@click.option("-d", "--dict", is_flag=True)
@click.option("-s", "--shuffle", type=float, default=0.0)
@click.option(
    "-u",
    "--shuffle-unit",
    "shuffle_unit_option",
    type=click.Choice(["8", "16"]),
    default="8",
)
@click.option("-v", "--verbose", is_flag=True)
def main(readfile, writefile, dict, shuffle, shuffle_unit_option, verbose):
    global use_hr_dict
    global shuffle_percent
    global shuffle_unit
    global tracks_data
    global tempo_events
    global staff_num
    global time_signature_n
    global time_signature_d
    global staff_names
    global current_staff_id
    global pickup_offset
    global pending_pickup_len
    use_hr_dict = dict
    shuffle_percent = max(0.0, min(100.0, float(shuffle)))
    shuffle_unit = int(shuffle_unit_option)
    MP.DEBUG = verbose
    tracks_data = []
    tempo_events = []
    staff_num = 0
    time_signature_n = 0
    time_signature_d = 0
    staff_names = {}
    current_staff_id = None
    pickup_offset = 0
    pending_pickup_len = None
    MP.parse_xml(
        click.format_filename(readfile),
        set_staff_start,
        set_staff_end,
        set_staff_name,
        set_measure_len,
        set_time_signature,
        set_pitch,
        set_rest,
        set_lyric,
        set_tie,
        set_dot,
        set_tempo,
        set_tuplet,
    )
    project = build_project_data(tracks_data)
    json_output = json.dumps(project, ensure_ascii=True)
    write_to_file(click.format_filename(writefile), json_output)


if __name__ == "__main__":
    main()
