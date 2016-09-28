var inputUrl = document.getElementById('inputUrl');

document.getElementById('playNow').onclick = function() {
    if (inputUrl.validity.valid) {
        playVideoNow(inputUrl.value);
    }
}


document.getElementById('playLater').onclick = function() {
    if (inputUrl.validity.valid) {
        addToPlaylist(inputUrl.value);
    }
}


document.getElementById('btn-next').onclick = function() {
    var request = new XMLHttpRequest();
    request.open('GET', '/player/' + playerId + '/next');
    request.send();
}


document.getElementById('btn-prev').onclick = function() {
    var request = new XMLHttpRequest();
    request.open('GET', '/player/' + playerId + '/prev');
    request.send();
}


document.getElementById('btn-play').onclick = function() {
    var request = new XMLHttpRequest();
    request.open('GET', '/player/' + playerId + '/play');
    request.send();
}


document.getElementById('btn-pause').onclick = function() {
    var request = new XMLHttpRequest();
    request.open('GET', '/player/' + playerId + '/pause');
    request.send();
}


function playVideoNow(videoURL){
    var parsedURL = new URL(videoURL);
    var videoId = parsedURL.searchParams.get('v');

    var request = new XMLHttpRequest();
    request.open('GET', '/player/' + playerId + '/play/' + videoId);
    request.send();

}


function addToPlaylist(videoURL){
    var parsedURL = new URL(videoURL);
    var videoId = parsedURL.searchParams.get('v');

    var request = new XMLHttpRequest();
    request.open('GET', '/player/' + playerId + '/playlist/add/' + videoId);
    request.send();
}
