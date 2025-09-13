import logging
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import jukebox.plugs as plugin
import jukebox.cfghandler

logger = logging.getLogger('jb.spotify')
cfg = jukebox.cfghandler.get_handler('jukebox')

SPOTIPY_CLIENT_ID = cfg.get('spotify', 'client_id')
SPOTIPY_CLIENT_SECRET = cfg.get('spotify', 'client_secret')
SPOTIPY_REDIRECT_URI = cfg.get('spotify', 'redirect_uri')

scope = 'user-read-playback-state,user-modify-playback-state,user-read-currently-playing'

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=SPOTIPY_CLIENT_ID,
                                               client_secret=SPOTIPY_CLIENT_SECRET,
                                               redirect_uri=SPOTIPY_REDIRECT_URI,
                                               scope=scope))


@plugin.register
def play_spotify_track(track_uri: str):
    """Play a Spotify track given its URI"""
    try:
        sp.start_playback(uris=[track_uri])
        logger.info(f"Playing Spotify track: {track_uri}")
    except Exception as e:
        logger.error(f"Failed to play Spotify track: {e}")


@plugin.register
def pause_spotify_playback():
    """Pause Spotify playback"""
    try:
        sp.pause_playback()
        logger.info("Paused Spotify playback")
    except Exception as e:
        logger.error(f"Failed to pause Spotify playback: {e}")


@plugin.register
def resume_spotify_playback():
    """Resume Spotify playback"""
    try:
        sp.start_playback()
        logger.info("Resumed Spotify playback")
    except Exception as e:
        logger.error(f"Failed to resume Spotify playback: {e}")


def initialize():
    """Initialize the Spotify module"""
    global sp
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=SPOTIPY_CLIENT_ID,
                                                   client_secret=SPOTIPY_CLIENT_SECRET,
                                                   redirect_uri=SPOTIPY_REDIRECT_URI,
                                                   scope=scope))
    logger.info("Spotify module initialized")
