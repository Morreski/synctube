
document.getElementById('choose-player').onclick = function() {
  var playerName = prompt('Please choose a name for your player.');
  if (playerName === null) {
    return;
  }
  window.location = 'player/' + playerName;
}

document.getElementById('choose-controller').onclick = function() {
  var playerName = prompt('Please enter name of the player that you want to connect to.');
  if (playerName === null) {
    return;
  }
  window.location = 'controller/' + playerName;
}
