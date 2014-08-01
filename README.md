Likes XSPF
==========

Commandline tool that generates XSPF playlists for SoundCloud likes. XSPF playlists are supported in a [huge number of applications](http://www.xspf.org/applications/).

Install
-------

likes_xspf uses the soundcloud API library. It can be installed as follows.

```
easy_install soundcloud
```

The script can now be run directly.

Usage
-----
usage: `likes_xspf [-h] [-o OUT] user_url`
* user_url           URL to the user's SoundCloud page
* -h, --help         show this help message and exit
* -o OUT, --out OUT  output filename
