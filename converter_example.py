#!/usr/bin/env python

import click
import re
from txt_colors import txt
import musescore_parser as MP
import jp_to_hr

ONE_BEAT = 705600000
TAB = '  '

time_signature_n = 0
time_signature_d = 0
pitch = 0
duration = 0
onset = 0
lyric = ''
last_lyric = ''
comment = ''
tie = False
dot = 0
staff_num = 0

output_string = ""
use_hr_dict = False

def get_time_signature_duration(n, d):
    # print("get_time_signature_duration")
    if (n == 4 and d == 4):
        return int(ONE_BEAT * 4)
    elif (n == 3 and d == 4):
        return int(ONE_BEAT * 3)
    elif (n == 6 and d == 8):
        return int(6 * int(ONE_BEAT / 2))

duration_type = {
    'measure' : None,
    'whole' : int(ONE_BEAT * 4),
    'half' : int(ONE_BEAT * 2),
    'quarter' : int(ONE_BEAT),
    'eighth' : int(ONE_BEAT / 2),
    '16th' : int(ONE_BEAT / 4),
    '32nd' : int(ONE_BEAT / 8)
}

def generate_lyric(l):
    if (l in ["-", "", '', None]):
        return "-"
    global use_hr_dict
    if (use_hr_dict):
        string = "."
        for letter in l:
            string += " " + jp_to_hr.jp_to_hr[letter.lower()]
        return string
    return re.sub(r'\W+', '', l)

def generate_project_start():
    string = ''
    string += '{' + '\n'
    string += '    "version": 7,' + '\n'
    string += '    "meter": [' + '\n'
    string += '        {' + '\n'
    string += '            "measure": 0,' + '\n'
    string += '            "beatPerMeasure": 4,' + '\n'
    string += '            "beatGranularity": 4' + '\n'
    string += '        }' + '\n'
    string += '    ],' + '\n'
    string += '    "tempo": [' + '\n'
    string += '        {' + '\n'
    string += '            "position": 0,' + '\n'
    string += '            "beatPerMinute": 90.0' + '\n'
    string += '        }' + '\n'
    string += '    ],' + '\n'
    string += '    "tracks": [' + '\n'
    return string

def generate_staff_start():
    global staff_num
    string = ''
    string += '        {' + '\n'
    string += '            "name": "Unnamed Track",' + '\n'
    string += '            "dbName": "Eleanor Forte",' + '\n'
    string += '            "color": "15e879",' + '\n'
    string += '            "displayOrder": ' + str(staff_num) + ',' + '\n'
    string += '            "dbDefaults": {},' + '\n'
    string += '            "notes": [' + '\n'
    return string

def generate_note():
    string = ''
    string += '                {' + '\n'
    string += '                    "onset": ' + str(onset) + ',' + '\n'
    string += '                    "duration": ' + str(duration) + ',' + '\n'
    string += '                    "lyric": "' + generate_lyric(lyric) + '",' + '\n'
    string += '                    "comment": "' + str(lyric) + '",' + '\n'
    string += '                    "pitch": ' + str(pitch) + '' + '\n'
    string += '                },' + '\n'
    return string

def generate_staff_end():
    string = ''
    string += '            ],' + '\n'
    string += '            "gsEvents": null,' + '\n'
    string += '            "mixer": {' + '\n'
    string += '                "gainDecibel": 0.0,' + '\n'
    string += '                "pan": 0.0,' + '\n'
    string += '                "muted": false,' + '\n'
    string += '                "solo": false,' + '\n'
    string += '                "engineOn": true,' + '\n'
    string += '                "display": true' + '\n'
    string += '            },' + '\n'
    string += '            "parameters": {' + '\n'
    string += '                "interval": 5512500,' + '\n'
    string += '                "pitchDelta": [' + '\n'
    string += '                    0,' + '\n'
    string += '                    0' + '\n'
    string += '                ],' + '\n'
    string += '                "vibratoEnv": [' + '\n'
    string += '                    0,' + '\n'
    string += '                    0' + '\n'
    string += '                ],' + '\n'
    string += '                "loudness": [' + '\n'
    string += '                    0,' + '\n'
    string += '                    0' + '\n'
    string += '                ],' + '\n'
    string += '                "tension": [' + '\n'
    string += '                    0,' + '\n'
    string += '                    0' + '\n'
    string += '                ],' + '\n'
    string += '                "breathiness": [' + '\n'
    string += '                    0,' + '\n'
    string += '                    0' + '\n'
    string += '                ],' + '\n'
    string += '                "voicing": [' + '\n'
    string += '                    0,' + '\n'
    string += '                    0' + '\n'
    string += '                ],' + '\n'
    string += '                "gender": [' + '\n'
    string += '                    0,' + '\n'
    string += '                    0' + '\n'
    string += '                ]' + '\n'
    string += '            }' + '\n'
    string += '        },' + '\n'
    return string

def generate_project_end():
    string = ''
    string += '    ],' + '\n'
    string += '    "instrumental": {' + '\n'
    string += '        "filename": "",' + '\n'
    string += '        "offset": 0.0' + '\n'
    string += '    },' + '\n'
    string += '    "mixer": {' + '\n'
    string += '        "gainInstrumentalDecibel": 0.0,' + '\n'
    string += '        "gainVocalMasterDecibel": 0.0,' + '\n'
    string += '        "instrumentalMuted": false,' + '\n'
    string += '        "vocalMasterMuted": false' + '\n'
    string += '    }' + '\n'
    string += '}' + '\n'
    return string

def set_staff_start():
    global onset
    onset = 0
    # print(generate_staff_start())
    global output_string
    output_string += generate_staff_start()
    
def set_staff_end():
    # print(generate_staff_end())
    global output_string
    output_string += generate_staff_end()
    global staff_num
    staff_num += 1

def set_time_signature(n, d):
    global time_signature_n
    time_signature_n = int(n)
    global time_signature_d
    time_signature_d = int(d)
    global duration_type
    duration_type['measure'] = get_time_signature_duration(time_signature_n, time_signature_d)

def set_pitch(p, d):
    global pitch
    global duration
    global output_string
    global onset
    global lyric
    global tie
    global dot

    pitch = int(p)
    duration += duration_type[d]

    if (dot > 0):
        duration += int(duration_type[d] / 2)
    if (dot > 1):
        duration += int(duration_type[d] / 4)
    if (dot > 2):
        duration += int(duration_type[d] / 8)
    dot = 0

    if (tie):
        tie = False
    else:
        if (lyric == ''):
            lyric = '-'
        # print(generate_note())
        output_string += generate_note()
        onset += duration
        duration = 0
        lyric = ''

def set_rest(d):
    global onset
    global dot
    if (dot > 0):
        duration += int(duration_type[d] / 2)
    if (dot > 1):
        duration += int(duration_type[d] / 4)
    if (dot > 2):
        duration += int(duration_type[d] / 8)
    dot = 0
    onset += duration_type[d]

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

def write_to_file(file_name, data):
    with open(file_name, "w") as write_file:
        write_file.write(data)

@click.command()
@click.argument('readfile', type=click.Path(exists=True))
@click.argument('writefile', type=click.Path(exists=False))
@click.option('-d', "--dict", is_flag=True)
def main(readfile, writefile, dict):
    global output_string
    global use_hr_dict
    use_hr_dict = dict
    output_string += generate_project_start()
    MP.parse_xml(click.format_filename(readfile), set_staff_start, set_staff_end, set_time_signature, set_pitch, set_rest, set_lyric, set_tie, set_dot)
    output_string += generate_staff_end()
    output_string += generate_project_end()
    write_to_file(click.format_filename(writefile), output_string)

if __name__ == '__main__':
    main()