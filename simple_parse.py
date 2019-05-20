#!/usr/bin/env python

from txt_colors import txt
import musescore_parser as MP

ONE_BEAT = 705600000
TAB = '  '

time_signature_n = 0
time_signature_d = 0
pitch = 0
duration = 0
onset = 0
lyric = ''
comment = ''

output_string = ""

def get_time_signature_duration(n, d):
    if (n == 4 and n == 4):
        return int(ONE_BEAT * 4)
    elif (n == 3 and n == 4):
        return int(ONE_BEAT * 3)
    elif (n == 6 and n == 8):
        return int(6 * int(ONE_BEAT / 2))

duration_type = {
    'measure' : get_time_signature_duration(time_signature_n, time_signature_d),
    'whole' : int(ONE_BEAT * 4),
    'half' : int(ONE_BEAT * 2),
    'quarter' : int(ONE_BEAT),
    'eighth' : int(ONE_BEAT / 2),
    '16th' : int(ONE_BEAT / 4),
    '32nd' : int(ONE_BEAT / 8)
}

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
    string += '            "beatPerMinute": 140.0' + '\n'
    string += '        }' + '\n'
    string += '    ],' + '\n'
    string += '    "tracks": [' + '\n'
    return string

def generate_staff_start():
    string = ''
    string += '        {' + '\n'
    string += '            "name": "Unnamed Track",' + '\n'
    string += '            "dbName": "",' + '\n'
    string += '            "color": "15e879",' + '\n'
    string += '            "displayOrder": 0,' + '\n'
    string += '            "dbDefaults": {},' + '\n'
    string += '            "notes": [' + '\n'
    return string

def generate_note():
    string = ''
    string += '                {' + '\n'
    string += '                    "onset": ' + str(onset) + ',' + '\n'
    string += '                    "duration": ' + str(duration) + ',' + '\n'
    string += '                    "lyric": "' + str(lyric) + '",' + '\n'
    string += '                    "comment": "' + comment + '",' + '\n'
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
    print(txt.CRED + "set_staff_start" + txt.CEND)
    print(generate_staff_start())
    global output_string
    output_string += generate_staff_start()
    
def set_staff_end():
    print(txt.CRED + "set_staff_end" + txt.CEND)
    print(generate_staff_end())
    global output_string
    output_string += generate_staff_end()

def set_time_signature(n, d):
    print(txt.CRED + "set_time_signature" + txt.CEND, n, d)
    global time_signature_n
    time_signature_n = int(n)
    global time_signature_d
    time_signature_d = int(d)

def set_pitch(p, d):
    print(txt.CRED + "set_pitch" + txt.CEND, p, d)
    global pitch
    pitch = int(p)
    global duration
    duration = duration_type[d]
    print(generate_note())
    global output_string
    output_string += generate_note()
    global onset
    onset += duration

def set_rest(d):
    print(txt.CRED + "set_rest" + txt.CEND, d)
    global onset
    onset += duration

def write_to_file(file_name, data):
    with open(file_name, "w") as write_file:
        write_file.write(data)

print(generate_project_start())
output_string += generate_project_start()
MP.parse_xml('examples/musicxml.mscx', set_staff_start, set_staff_end, set_time_signature, set_pitch, set_rest)
print(generate_project_end())
output_string += generate_project_end()

write_to_file("test.json", output_string)