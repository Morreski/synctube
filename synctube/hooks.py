def hook_play_next(player, event):
    pos = player.position_in_playlist
    if pos is None:
        next_song = player.playlist.first
    else:
        next_song = player.playlist[pos]['next']
    player.position_in_playlist = next_song


def hook_play_prev(player, event):
    pos = player.position_in_playlist
    if pos is None:
        prev_song = None
    else:
        prev_song = player.playlist[pos]['prev']
    player.position_in_playlist = prev_song
