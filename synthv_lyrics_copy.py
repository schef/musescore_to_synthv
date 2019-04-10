#!/usr/bin/env python3

import json
import sys

ONE_BEAT = 705600000
BEATS_IN_BAR = 4
THIRTYSECOND_NOTES_IN_BEAT = 8


def read_file(file_name):
    with open(file_name, "r") as read_file:
        data = json.load(read_file)
    return data


def write_file(file_name, data):
    with open(file_name, "w") as write_file:
        json.dump(data, write_file)


def get_track_names(data):
    track_names = []
    for track in data['tracks']:
        track_names.append(track['name'])
    return track_names


def get_track_by_name(data, track_name):
    for track in data['tracks']:
        if track['name'] == track_name:
            return track


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


if __name__ == "__main__":
    # if not (len(sys.argv) > 2):
        # print("Usage:")
        # print("    " + sys.argv[0] + " <infile> <outfile>")
        # sys.exit(0)
    infile = sys.argv[1]
    data = read_file(infile)

    start_bar = input("Start bar [0]: ")
    if not start_bar:
        start_bar = 0
    start_bar = int(start_bar)

    start_beat = input("Start beat [0]: ")
    if not start_beat:
        start_beat = 0
    start_beat = int(start_beat)

    end_bar = input("End bar [10]: ")
    if not end_bar:
        end_bar = 10
    end_bar = int(end_bar)

    end_beat = input("End beat [0]: ")
    if not end_beat:
        end_beat = 10
    end_beat = int(end_beat)

    track_names = get_track_names(data)
    print(track_names)

    track_from = input("Track name to copy from [" + track_names[0] + "]: ")
    if not track_from:
        track_from = track_names[0]

    # track_to = input("Track name to copy to [" + track_names[1] + "]: ")
    # if not track_to:
        # track_to = track_names[1]

    # if not (track_from in track_names) or not (track_to in track_names):
        # print("Unvalid track name")
        # sys.exit(0)

        track_to = []

    data_edit = edit_lyrics(data, start_bar, start_beat,
                            end_bar, end_beat, track_from, track_to)

    # outfile = sys.argv[2]
    # write_file(outfile, data_edit)
