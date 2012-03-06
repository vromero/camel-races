function Racecourse(race_key, racecourseTableQuery) {
	this.race_key = race_key;
	this.racecourseTable = $(racecourseTableQuery);
	
	this.setRunnerStatus = function(runner_key, status) {
		runner_element = $("#" + my_runner_key + '-name')

		// Show the status in the runner name
		if(status) {
			weight = 'bolder'
		} else {
			weight = 'normal'
		}
		runner_element.css('font-weight', weight);
	}

	this.setRunnerPosition = function(runner_key, position) {
		runner_element = this.getRunnerElement(runner_key, false);

		$("#" + runner_key + '-progress').animate({
			rotate : '-15deg'
		}, 150).animate({
			rotate : '+15deg'
		}, 150)
		$("#" + runner_key + '-progress').animate({
			left : position + '%',
			rotate : '0deg'
		}, 300, 'swing');

		$("#" + runner_key + '-progress').fadeIn();
	}

	this.removeRunner = function(runner_key) {
		runner_element = this.getRunnerElement(runner_key, false);
		if(runner_element.length != 0) {
			$("#" + runner_key).hide("explode", {
				pieces : 16
			}, 1000);
		}
	}
	

	this.getRunnerElement = function(runner_key, createIfNotExist) {
		runner_element = $("#" + runner_key)
		if(runner_element.length == 0 && createIfNotExist) {
			$.ajax({
				url : "/race/" + race_key + "/runner/" + runner_key,
				success : function(results) {
					$('#racetrack_table').append(results)
					$("#" + my_runner_key).fadeIn();
				}
			});
		}
		return runner_element;
	}




}