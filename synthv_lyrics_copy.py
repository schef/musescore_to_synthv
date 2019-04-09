#!/usr/bin/env python3

import json
import sys

def read_file(file_name):
    with open(file_name, "r") as read_file:
        data = json.load(read_file)
    return data

def write_file(file_name, data):
    with open(file_name, "w") as write_file:
        json.dump(data, write_file)

def edit_lyrics(data):
    for track in data['tracks']:
        print(track['name'])
        # for note in track['notes']:
            # print(note)
    return data

if __name__ == "__main__":
    # if not (len(sys.argv) > 2):
        # print("Usage:")
        # print("    " + sys.argv[0] + " <infile> <outfile>")
        # sys.exit(0)
    infile = sys.argv[1]
    # outfile = sys.argv[2]
    data = read_file(infile)
    dataa = edit_lyrics(data)
    # write_file(outfile, dataa)