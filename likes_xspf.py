#!/usr/bin/env python3
import soundcloud
import itertools
import xml.etree.ElementTree as ET
import argparse

CLIENT_ID = "e818e8c85bb8ec3e90a9bbca23ca5e2a"

def write_playlist(user_url, outfile=None):
    client = soundcloud.Client(client_id = CLIENT_ID)

    print("Resolving URL: {url}".format(url=user_url))
    user = client.get("/resolve", url=user_url)
    print("Found User: {name}".format(name=user.username))

    playlist_root = ET.Element("playlist", version="1", xmlns="http://xspf.org/ns/0/")
    tree = ET.ElementTree(element=playlist_root)
    tracklist_root = ET.SubElement(playlist_root, "trackList")

    for i in itertools.count():
        likes = client.get("/users/{id}/favorites".format(id=user.id),
                           offset = i*50, limit = 50)

        if len(likes) == 0:
            break

        count = 0
        for track in likes:
            if "stream_url" not in track.keys():
                break
            track_node = ET.SubElement(tracklist_root, "track")

            title_node = ET.SubElement(track_node, "title")
            title_node.text = track.title

            location_node = ET.SubElement(track_node, "location")
            location_node.text = "{url}?client_id={client_id}".format(url=track.stream_url, client_id=CLIENT_ID)

            creator_node = ET.SubElement(track_node, "creator")
            creator_node.text = track.user["username"]

            image_node = ET.SubElement(track_node, "image")
            image_node.text = track.artwork_url

            duration_node = ET.SubElement(track_node, "duration")
            duration_node.text = str(track.duration)

            count += 1

        print("Processed {count}/{total} tracks from page #{page_num}".format(count=count, total=len(likes), page_num = (i+1)))

    outfile = "{id}_likes.xspf".format(id=user.id) if outfile is None else outfile
    print("Writing Playlist {filename}".format(filename=outfile))
    tree.write(outfile, encoding="UTF-8", xml_declaration=True)
    
if __name__ == "__main__":
    ap = argparse.ArgumentParser(prog="likes_xspf", description="Generate XSPF (XML Shareable Playlist Format) file for a SoundCloud user's liked tracks")
    ap.add_argument("-o", "--out", help="output filename")
    ap.add_argument("user_url", help="URL to the user's SoundCloud page")

    opts = ap.parse_args()
    write_playlist(opts.user_url, opts.out)
