#!/usr/bin/env python3

import json
import sys
import click
import xmltodict

ONE_BEAT = 705600000
BEATS_IN_BAR = 4
THIRTYSECOND_NOTES_IN_BEAT = 8


class txt:
    ENDC = '\033[0m'
    CBOLD = '\33[1m'
    CITALIC = '\33[3m'
    CURL = '\33[4m'
    CBLINK = '\33[5m'
    CBLINK2 = '\33[6m'
    CSELECTED = '\33[7m'

    CBLACK = '\33[30m'
    CRED = '\33[31m'
    CGREEN = '\33[32m'
    CYELLOW = '\33[33m'
    CBLUE = '\33[34m'
    CVIOLET = '\33[35m'
    CBEIGE = '\33[36m'
    CWHITE = '\33[37m'

    CBLACKBG = '\33[40m'
    CREDBG = '\33[41m'
    CGREENBG = '\33[42m'
    CYELLOWBG = '\33[43m'
    CBLUEBG = '\33[44m'
    CVIOLETBG = '\33[45m'
    CBEIGEBG = '\33[46m'
    CWHITEBG = '\33[47m'

    CGREY = '\33[90m'
    CRED2 = '\33[91m'
    CGREEN2 = '\33[92m'
    CYELLOW2 = '\33[93m'
    CBLUE2 = '\33[94m'
    CVIOLET2 = '\33[95m'
    CBEIGE2 = '\33[96m'
    CWHITE2 = '\33[97m'

    TAB = '    '


def read_json_file(file_name):
    with open(file_name, "r") as read_file:
        data = json.load(read_file)
    return data


def write_json_file(file_name, data):
    with open(file_name, "w") as write_file:
        json.dump(data, write_file)


def read_xml_file(file_name):
    with open(file_name, "r") as read_file:
        data = read_file.read()
    return xmltodict.parse(data)

def get_track_names(data):
    track_names = []
    for track in data['tracks']:
        track_names.append(track['name'])
    return track_names


def get_track_by_name(data, track_name):
    for track in data['tracks']:
        if track['name'] == track_name:
            return track


def get_track_by_index(data, index):
    return data['tracks'][index]


def set_track_by_name(data, track_edit, track_name):
    for track in data['tracks']:
        if track['name'] == track_name:
            track = track_edit
    return data


def get_time_from_onset(onset):
    number_of_beats = int(onset / ONE_BEAT)
    number_of_bars = int(number_of_beats / BEATS_IN_BAR)
    number_of_beats_in_last_bar = (
        number_of_beats - (number_of_bars * BEATS_IN_BAR))
    number_of_thirtysecond_notes_left_in_last_bar = round(
        ((onset / ONE_BEAT) - number_of_beats) / 0.125, 2)
    return (number_of_bars + 1, number_of_beats_in_last_bar + 1, number_of_thirtysecond_notes_left_in_last_bar + 1)


def get_thirtysecond_total_from_onset(onset):
    bars, beats, thirtysecond = get_time_from_onset(onset)
    beats_total = (bars - 1) * BEATS_IN_BAR + beats - 1
    thirtysecond_total = beats_total * THIRTYSECOND_NOTES_IN_BEAT + thirtysecond
    return (thirtysecond_total)


def edit_lyrics(data, start_bar, start_beat, end_bar, end_beat, track_from, track_to):
    track_from_data = get_track_by_name(data, track_from)
    track_to_data = get_track_by_name(data, track_to)
    print(track_from)
    for note in track_from_data['notes']:
        bars, beats, thirtysecond = get_time_from_onset(note['onset'])
        print(bars, beats, thirtysecond)
        thirtysecond_total = get_thirtysecond_total_from_onset(note['onset'])
        print(thirtysecond_total)
    data = set_track_by_name(data, track_to_data, track_to)
    return data


@click.group()
def main():
    pass


@click.command()
@click.argument('infile', type=click.Path(exists=True))
@click.option('-t', '--track', prompt=True)
def info(infile):
    click.echo(txt.CBOLD + "Info:" + txt.ENDC + " " + infile)
    infile_content = read_json_file(infile)

    click.echo(txt.CBOLD + "Tracks:" + txt.ENDC)
    track_names = get_track_names(infile_content)
    for e, name in enumerate(track_names):
        click.echo(txt.TAB + '[' + str(e) + '] ' + name)


main.add_command(info)

# if __name__ == "__main__":
    # main()
    # if not (len(sys.argv) > 2):
    # print("Usage:")
    # print("    " + sys.argv[0] + " <infile> <outfile>")
    # sys.exit(0)
    # infile = sys.argv[1]
    # data = read_file(infile)

    # start_bar = input("Start bar [0]: ")
    # if not start_bar:
    #     start_bar = 0
    # start_bar = int(start_bar)

    # start_beat = input("Start beat [0]: ")
    # if not start_beat:
    #     start_beat = 0
    # start_beat = int(start_beat)

    # end_bar = input("End bar [10]: ")
    # if not end_bar:
    #     end_bar = 10
    # end_bar = int(end_bar)

    # end_beat = input("End beat [0]: ")
    # if not end_beat:
    #     end_beat = 10
    # end_beat = int(end_beat)

    # track_names = get_track_names(data)
    # print(track_names)

    # track_from = input("Track name to copy from [" + track_names[0] + "]: ")
    # if not track_from:
    #     track_from = track_names[0]

    # track_to = input("Track name to copy to [" + track_names[1] + "]: ")
    # if not track_to:
    # track_to = track_names[1]

    # if not (track_from in track_names) or not (track_to in track_names):
    # print("Unvalid track name")
    # sys.exit(0)

    #     track_to = []

    # data_edit = edit_lyrics(data, start_bar, start_beat,
    #                         end_bar, end_beat, track_from, track_to)

    # outfile = sys.argv[2]
    # write_file(outfile, data_edit)
