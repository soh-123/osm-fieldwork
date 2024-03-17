#!/usr/bin/python3

# Copyright (c) 2022, 2023 Humanitarian OpenStreetMap Team
#
# This file is part of osm_fieldwork.
#
#     Underpass is free software: you can redistribute it and/or modify
#     it under the terms of the GNU General Public License as published by
#     the Free Software Foundation, either version 3 of the License, or
#     (at your option) any later version.
#
#     Underpass is distributed in the hope that it will be useful,
#     but WITHOUT ANY WARRANTY; without even the implied warranty of
#     MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#     GNU General Public License for more details.
#
#     You should have received a copy of the GNU General Public License
#     along with osm_fieldwork.  If not, see <https:#www.gnu.org/licenses/>.
#
"""Test functionalty of basemapper.py."""

import logging
import os
import shutil

from osm_fieldwork.basemapper import BaseMapper
from osm_fieldwork.sqlite import DataFile
from io import BytesIO


log = logging.getLogger(__name__)

rootdir = os.path.dirname(os.path.abspath(__file__))
boundary = f"{rootdir}/testdata/Rollinsville.geojson"
outfile = f"{rootdir}/testdata/rollinsville.mbtiles"
base = "./tiles"

# boundary = open(infile, "r")
# poly = geojson.load(boundary)
# if "features" in poly:
#    geometry = shape(poly["features"][0]["geometry"])
# elif "geometry" in poly:
#    geometry = shape(poly["geometry"])
# else:
#    geometry = shape(poly)


def test_create_boundary_bytesio():
    """See if the file got loaded."""
    with open(boundary, "rb") as geojson_file:
        boundary_bytesio = geojson_file.read()  # read as a `bytes` object.
        boundary_bytesio = BytesIO(boundary_bytesio)
    hits = 0
    basemap = BaseMapper(boundary_bytesio, base, "topo", False)
    tiles = list()
    for level in [8, 9, 10, 11, 12]:
        basemap.getTiles(level)
        tiles += basemap.tiles

    if len(tiles) == 5:
        hits += 1

    if tiles[0].x == 52 and tiles[1].y == 193 and tiles[2].x == 211:
        hits += 1

    outf = DataFile(outfile, basemap.getFormat())
    outf.writeTiles(tiles, base)

    os.remove(outfile)
    shutil.rmtree(base)

    assert hits == 2

def test_valid_boundary_string():
    """See if the file got loaded."""
    boundary_str = "-4.730494,41.650541,-4.725634,41.652874"
    hits = 0
    basemap = BaseMapper(boundary_str, base, "topo", False)
    tiles = list()
    for level in [8, 9, 10, 11, 12]:
        basemap.getTiles(level)
        tiles += basemap.tiles

    if len(tiles) == 5:
        hits += 1

    if tiles[0].x == 52 and tiles[1].y == 193 and tiles[2].x == 211:
        hits += 1

    outf = DataFile(outfile, basemap.getFormat())
    outf.writeTiles(tiles, base)

    os.remove(outfile)
    shutil.rmtree(base)

    assert hits == 2

def test_invalid_boundary_string():
    """See if the file got loaded."""
    hits = 0
    try:
        basemap = BaseMapper(boundary, base, "topo", False)
        tiles = list()
        for level in [8, 9, 10, 11, 12]:
            basemap.getTiles(level)
            tiles += basemap.tiles

        if len(tiles) == 5:
            hits += 1

        if tiles[0].x == 52 and tiles[1].y == 193 and tiles[2].x == 211:
            hits += 1

        outf = DataFile(outfile, basemap.getFormat())
        outf.writeTiles(tiles, base)

        os.remove(outfile)
        shutil.rmtree(base)
    except ValueError as e:
        hits += 1

    assert hits == 1

if __name__ == "__main__":
    test_create_boundary_bytesio()
    test_valid_boundary_string()
    test_invalid_boundary_string()
