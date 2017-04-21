# -*- coding: utf-8 -*-
"""
Created on Thu Mar 10 21:19:16 2016

@author: csx
add some edits in github

read the itune track library data from XML file. saved data into self built SQLite database.
"""
import xml.etree.ElementTree as ET
import sqlite3

conn = sqlite3.connect("trackdb_library.sqlite")
cur = conn.cursor()

cur.executescript('''
DROP TABLE IF EXISTS Artist;
DROP TABLE IF EXISTS Album;
DROP TABLE IF EXISTS Track;
DROP TABLE IF EXISTS Genre;

CREATE TABLE Artist (
    id  INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    name    TEXT UNIQUE
);

CREATE TABLE Genre (
    id  INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    name    TEXT UNIQUE
);

CREATE TABLE Album (
    id  INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    artist_id  INTEGER,
    title   TEXT UNIQUE
);

CREATE TABLE Track (
    id  INTEGER NOT NULL PRIMARY KEY 
        AUTOINCREMENT UNIQUE,
    title TEXT  UNIQUE,
    album_id  INTEGER,
    genre_id  INTEGER,
    len INTEGER, rating INTEGER, count INTEGER
);
''')

def lookup(track,key):
    found = False
    for child in track:
        if found: return child.text
        if child.tag == "key" and child.text == key:
            found = True 

library = ET.parse("Library.xml")
tracks = library.findall("dict/dict/dict")
print "dict count",len(tracks)
for track in tracks:
    if ( lookup(track, 'Track ID') is None ) : continue
    name = lookup(track, 'Name')
    artist = lookup(track, 'Artist')
    album = lookup(track, 'Album')
    count = lookup(track, 'Play Count')
    rating = lookup(track, 'Rating')
    length = lookup(track, 'Total Time')
    genre = lookup(track, 'Genre')

    if name is None or artist is None or album is None or genre is None: 
        continue
    
    cur.execute("INSERT OR IGNORE INTO Artist(name) VALUES (?)",(artist,))    
    cur.execute("SELECT id FROM Artist WHERE name=?",(artist,))
    artist_id = cur.fetchone()[0]
    cur.execute("INSERT OR IGNORE INTO Album(artist_id,title) VALUES (?,?)",
                (artist_id,album,))
    cur.execute("SELECT id FROM Album WHERE title = ?",(album,))
    album_id = cur.fetchone()[0]
    cur.execute("INSERT OR IGNORE INTO Genre(name) VALUES (?)",(genre,))
    cur.execute("SELECT id FROM Genre WHERE name = ?",(genre,))
    genre_id = cur.fetchone()[0]
    cur.execute('''INSERT OR IGNORE INTO Track(title,album_id,genre_id,len,rating,count)
                VALUES (?,?,?,?,?,?)''',(name,album_id,genre_id,length,rating,count,))
conn.commit()
conn.close()
                
