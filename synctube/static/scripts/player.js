let eventSourceURL = '/player/' + playerId + '/subscribe'
let es = new EventSource(eventSourceURL);
let player;


es.addEventListener('play_now', function(evt){
    data = JSON.parse(evt.data);
    playVideo(data.video_id);
});

es.addEventListener('play', function(evt){
    player.playVideo();
});


es.addEventListener('pause', function(evt){
    player.pauseVideo();
});

es.addEventListener('playlist_updated', function(evt){
    refreshPlaylist();
});

es.addEventListener('play_next', function(evt){
    playNextVideo();
});


es.addEventListener('play_prev', function(evt){
    playNextVideo(true);
});


function playNextVideo(reverse) {
    let reversed = reverse || false;
    let request = new XMLHttpRequest();
    let command = (reversed) ? 'prev' : 'next';
    request.open('GET', '/player/' + playerId + '/playlist/' + command);
    request.onload = function (evt) {
      if (evt.target.status === 200) {
          playVideo(evt.target.response)
      }
    }
    request.send();
}


function playVideo(videoId) {

    if (player != undefined) {
        player.destroy()
    }

				player = new YT.Player('player-container', {
        height: '390',
        width: '640',
        videoId: videoId,
        events: {
          'onReady': onPlayerReady,
          'onStateChange': onPlayerStateChange
								}
				});

				// autoplay video
				function onPlayerReady(event) {
        event.target.playVideo();
        refreshPlaylist();
				}

				// when video ends
				function onPlayerStateChange(event) {
        if(event.data === 0) {
            playNextVideo()
        }
				}
}


function displayPlaylistContent(videos) {
    let container = document.getElementById('playlist-container');
    let ul = document.createElement('ul');
    videos.forEach((video_id) => {
        let li = document.createElement('li');
        li.innerText = video_id;
        console.log(player.getVideoData().video_id)
        console.log(video_id)
        if (video_id === player.getVideoData().video_id) {
            li.style = 'color: red';
        }
        ul.appendChild(li);
    })
    while (container.firstChild) {
        container.removeChild(container.firstChild);
    }
    container.appendChild(ul);
}


function refreshPlaylist() {
    fetch('/playlist/' + playerId)
    .then((resp) => {
        return resp.json();
    })
    .then((playlist) => {
        displayPlaylistContent(playlist.videos);
    });
}
