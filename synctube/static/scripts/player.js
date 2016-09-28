var eventSourceURL = '/player/' + playerId + '/subscribe'
var es = new EventSource(eventSourceURL);
var player;


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


es.addEventListener('play_next', function(evt){
    playNextVideo();
});


es.addEventListener('play_prev', function(evt){
    playNextVideo(true);
});


function playNextVideo(reversed) {
    var reversed = reversed || false;
    var request = new XMLHttpRequest();
    var command = (reversed) ? 'prev' : 'next';
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
				}

				// when video ends
				function onPlayerStateChange(event) {
        if(event.data === 0) {
            playNextVideo()
        }
				}

}
