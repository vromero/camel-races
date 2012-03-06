

function Minigame(started, playAreaQuery, targetQuery) {
	this.playArea = $(playAreaQuery);
	this.target = $(targetQuery);
	this.score = 0;
	this.timeToAutoChange = 3000;
	this.timeoutID;
	this.started = started;
	this.score_callback = function(score) {};

	// To be used when x points are scored
	this.increaseScore = function(inc) {
		if (!this.started) {
			return;
		}
		this.setScore(this.score + inc);
		this.score_callback(this.score);	
	}

	this.setScore = function(score) {
		this.score = score;
		this.changeToRandomPos();		
		//this.playArea.css("background-image", 'url(' + this.calc_background(this.score) + ')');  
	}
	

	this.changeToRandomPos = function() {
		posx = Math.floor(Math.random() * (this.playArea.width() - this.target.width()));
		posy = Math.floor(Math.random() * (this.playArea.height() - this.target.height()));
		return this.moveElement(posx, posy);
	}

	this.moveElement = function(toX, toY) {
		var elem = document.getElementById("archery");
		elem.style.position = "relative";

		this.target.animate({
			left : toX + "px",
			top : toY + "px",
		}, 100);
		
		clearTimeout(this.timeoutID)
		this.timeoutID = setTimeout(this.changeToRandomPos.bind(this), this.timeToAutoChange);
	}

	this.finish = function() {
		this.target.fadeOut();
	}

	this.start = function() {
		this.started = true;
		this.target.hide();
		document.getElementById('archery').style.visibility = "visible";
		this.target.fadeIn();
		this.changeToRandomPos();
	}

	this.hide = function() {
		this.target.fadeOut();
	}

if (this.started) {
		this.start()
	}
}
