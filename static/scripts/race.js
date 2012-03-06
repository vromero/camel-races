var camel_minigame;
var readyPanel;
var racecourse;

// Network events
function handle_start(updateJson) {
	camel_minigame.start();
	readyPanel.receivedStart();
}

function handle_finish(finishJson) {
	readyPanel.receivedFinish();
}

function handle_update(updateJson) {
	payload = updateJson["payload"];

	for(my_runner_key in payload) {
		racecourse.setRunnerPosition(my_runner_key, payload[my_runner_key])
	}
}

function handle_disconnected(updateJson) {
	payload = updateJson["payload"];

	for(my_runner_key in payload) {
		racecourse.removeRunner(my_runner_key);
	}
}

function handle_runner_status(updateJson) {
	payload = updateJson["payload"];

	for(my_runner_key in payload) {
		status = payload[my_runner_key]

		racecourse.setRunnerStatus(my_runner_key, status);

		// If the update it´s for us toggle the button
		if(runner_key == my_runner_key) {
			readyPanel.receivedStatus(status);
		}

	}
}

function dispatch_message(data) {
	jsonData = jQuery.parseJSON(data.data);
	switch (jsonData["messageType"]) {

		case "gameUpdate":
			handle_update(jsonData)
			break;

		case "start":
			handle_start(jsonData)
			break;

		case "finish":
			handle_finish(jsonData)
			break;

		case "runnerStatusUpdate":
			handle_runner_status(jsonData);
			break;

		case "runnerDisconnected":
			handle_disconnected(jsonData);
			break;
	}
}

// Sender
function send_update_position(position) {
	$.ajax({
		url : '/rest/runner/' + runner_key,
		type : 'POST',
		data : '{"messageType" : "gameUpdate", "payload" : {"' + runner_key + '" : ' + position + '}	}',
	});
}

// Buttons
function click_share(finishJson) {
	$('#share').hide();
	$.blockUI({
		message : $('#share')
	});
}

// GAE Channel
function setup_google_channel() {
	channel = new goog.appengine.Channel(channel_token);
	socket = channel.open();
	socket.onmessage = dispatch_message;
	socket.onerror = channel_error;
	socket.onclose = channel_error;
}

function channel_error() {
	alert("There was an error on the communication channel")
}

// Main
$(document).ready(function() {
	var started = false;

	if(race_status == "finished") {
		started = true;
	}
	racecourse = new Racecourse(race_key, "#racetrack_table")
	camel_minigame = new Minigame(started, "#playarea", "#archery")
	camel_minigame.score_callback = send_update_position;
	readyPanel = new RunnerReadyPanel(runner_key, "#ready_panel", "#unready_panel", "#playarea", "#countdown_ready", "#countdown_steady", "#countdown_go", "#podium");

	$(function() {
		$("#share_button").button();
		$("#share_button").click(click_share);
	});
	if(race_status == "lobby") {
		readyPanel.lobby(runner_ready);
	} else if(race_status == "started") {
		readyPanel.start();
		camel_minigame.start();
	} else if(race_status == "finished") {
		readyPanel.finish();
	}

	setup_google_channel();
});
