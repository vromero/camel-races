function RunnerReadyPanel(runner_key, readyQuery, unreadyQuery, playAreaQuery, countDownReadyQuery, countDownSteadyQuery, countDownGoQuery, podiumQuery) {
	this.playArea = $(playAreaQuery);
	this.readyPanel = $(readyQuery);
	this.unreadyPanel = $(unreadyQuery);
	this.podiumPanel = $(podiumQuery);

	this.countDownReady = $(countDownReadyQuery);
	this.countDownSteady = $(countDownSteadyQuery);
	this.countDownGo = $(countDownGoQuery);

	this.runner_key = runner_key;

	this.send_ready_status = function(status) {
		$.ajax({
			url : '/rest/runner/' + runner_key,
			type : 'POST',
			data : '{"messageType" : "runnerStatusUpdate", "payload" : {"' + this.runner_key + '" : ' + status + '} }',
			contentType : 'application/vnd.start-race.json'
		});
	}

	this.requestReady = function() {
		this.send_ready_status(true)
	}

	this.requestUnready = function() {
		this.send_ready_status(false)
	}

	this.receivedStatus = function() {
		if(status) {
			this.receivedReady();
		} else {
			this.receivedUnready();
		}
	}

	this.receivedReady = function() {
		this.podiumPanel.hide();
		this.playArea.hide();
		this.unreadyPanel.hide();
		this.readyPanel.show();
	}

	this.receivedUnready = function() {
		this.podiumPanel.hide();
		this.playArea.hide();
		this.readyPanel.hide();
		this.unreadyPanel.show();
	}

	this.receivedStart = function() {
		this.countdown(this.start.bind(this))
	}

	this.receivedFinish = function() {
		updatePodiumContent = function(results) {
			this.podiumPanel.html(results)
		}

		$.ajax({
			url : "/race/" + race_key + "/podium",
			success : $.proxy(function(results) {
				this.podiumPanel.html(results)
			}, this)
		});

		this.playArea.hide();
		this.readyPanel.hide();
		this.unreadyPanel.hide();

		this.podiumPanel.fadeIn();
	}

	this.countdown = function(onFinish) {
		steadyAction = function() {
			this.countDownSteady.fadeIn().delay(1000).fadeOut(goAction.bind(this));
		}
		goAction = function() {
			this.countDownGo.fadeIn().delay(1000).fadeOut(playAction.bind(this));
		}
		playAction = function() {
			this.playArea.fadeIn();
		}

		this.playArea.hide();
		this.unreadyPanel.hide();
		this.readyPanel.hide();

		this.countDownReady.fadeIn().delay(1000).fadeOut(steadyAction.bind(this));
	}

	this.lobby = function(ready) {
		if(ready) {
			this.readyPanel.show();
			this.unreadyPanel.hide();
		} else {
			this.readyPanel.hide();
			this.unreadyPanel.show();
		}
		this.playArea.hide();
		this.podiumPanel.hide();
	}

	this.start = function() {
		this.readyPanel.hide();
		this.unreadyPanel.hide();
		this.playArea.show();
		this.podiumPanel.hide();
	}

	this.finish = function() {
		updatePodiumContent = function(results) {
			this.podiumPanel.html(results)
		}

		$.ajax({
			url : "/race/" + race_key + "/podium",
			success : $.proxy(function(results) {
				this.podiumPanel.html(results)
			}, this)
		});

		this.readyPanel.hide();
		this.unreadyPanel.hide();
		this.playArea.hide();
		this.podiumPanel.show();
	}

	this.unreadyPanel.click(this.requestReady.bind(this));
	this.readyPanel.click(this.requestUnready.bind(this));

}