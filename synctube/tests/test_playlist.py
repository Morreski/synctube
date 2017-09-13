from pytest import raises

from synctube.player import Playlist, PlaylistError


def test_append():
    p = Playlist()
    p.append('a')
    assert p.first == 'a'
    assert p.last == 'a'
    p.append('b')
    assert p.first == 'a'
    assert p.last == 'b'
    assert p['a']['next'] == 'b'


def test_ordering_ok():
    p = Playlist()
    p.append('a')
    p.append('b')
    p.append('c')

    assert list(p) == ['a', 'b', 'c']


def test_insert_after():
    p = Playlist()
    p.append('a')
    p.append('b')
    p.append('c')
    p.insert_after('b', 'z')

    assert list(p) == ['a', 'b', 'z', 'c']


def test_append_duplicate_error():
    p = Playlist()
    p.append('a')
    with raises(PlaylistError):
        p.append('a')


def test_insert_duplicate_error():
    p = Playlist()
    p.append('a')
    p.append('b')
    with raises(PlaylistError):
        p.insert_after('a', 'b')


def test_insert_key_error():
    p = Playlist()
    p.append('a')
    p.append('b')
    with raises(PlaylistError):
        p.insert_after('c', 'b')
