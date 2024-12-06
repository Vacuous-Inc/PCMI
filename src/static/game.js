/*

A JavaScript Blackjack game created June 2013 by Chris Clower 
(clowerweb.com). Deck class loosely based on a tutorial at:
http://www.codecademy.com/courses/blackjack-part-1

All graphics and code were designed/written by me except for the
chip box on the table, which was taken from the image at:
http://www.marketwallpapers.com/wallpapers/9/wallpaper-52946.jpg

Uses Twitter Bootstrap and jQuery, which also were not created by
me :)

Fonts used:
* "Blackjack" logo: Exmouth
* Symbol/floral graphics: Dingleberries
* All other fonts: Adobe Garamond Pro

All graphics designed in Adobe Fireworks CS6

You are free to use or modify this code for any purpose, but I ask
that you leave this comment intact. Please understand that this is
still very much a work in progress, and is not feature complete nor
without bugs.

I will also try to comment the code better for future updates :D

*/

/*MODIFIED FROM ABOVE*/

const socket = io("/play");

socket.on("connect", function() {
  console.log(socket.id); // x8WIv7-mJelg7on_ALbx
});


var player
socket.on("connected", function(data){
	
	player = new Player(data["sid"], data["name"], data["balance"]);

	console.log("Hi my name is " + player.name);

	$('#cash span').html(player.getCash());

	player.getBank();


});

var dealer
var text = document.getElementById("gameText");
socket.on("start", function(data) {
	//console.log("starting the game")
	text.innerText = "STARTING THE GAME";

	dealer = new Player(null, "dealer", 10000)
	console.log(data)
	dealer.setHand(new Card(...data["dealer"]["hand"][0]))
	dealer.setHand(new Card(...data["dealer"]["hand"][1]))
	dealer.handValue = data["dealer"]["value"];

});


/*
socket.on("game_event", function(data) {

  var parse = data

  if (parse.get("Player") == player.name){
  }
  
});
*/


socket.on("turn", function(data){
	console.log("its someones turn")
	console.log(data)

  if (data["Player"] == player.name){

	console.log("its my turn!");

	player.setHand(new Card(...data["Info"]["hand"][0]));
	player.setHand(new Card(...data["Info"]["hand"][1]));
	player.handValue = data["Info"]["value"];

	setActions("run");
	text.innerText = "Your turn " + player.name;

	showBoard()

  }
	
});




/*****************************************************************/
/*************************** Classes *****************************/
/*****************************************************************/


//PLAYER


class Player {

  	constructor(sid, name, balance){
		this.hand  = [],
		this.wager = 0,
		this.cash  = balance,
		this.bank  = 0,
		this.ele   = '',
		this.score = '',
		this.handValue = 0,
		this.name = name,
		this.sid = sid;
	}

	getElements() {
		if(this === player) {
			this.ele   = '#phand';
			this.score = '#pcard-0 .popover-content';
		} else {
			this.ele   = '#dhand';
			this.score = '#dcard-0 .popover-content';
		}

		return {'ele': this.ele, 'score': this.score};
	};

	getHand() {
			return this.hand;
		};

	setHand(card) {
			this.hand.push(card);
		};

 	resetHandfunction() {
			this.hand = [];
		};

	getWager() {
		return this.wager;
	};

	setWager(money) {
		this.wager += parseInt(money, 0);
	};

	resetWager() {
		this.wager = 0;
	};

	checkWager() {
		return this.wager <= this.cash ? true : false;
	};

	getCash() {
		return formatMoney(this.cash, 2, '.', ',');
	};

	setCash(money) {
		this.cash += money;
		this.updateBoard();
	};

	getBank() {
		$('#bank').html('Winnings: $' + formatMoney(this.bank, 2, '.', ','));

		if(this.bank < 0) {
			$('#bank').html('Winnings: <span style="color: #D90000">-$' + 
			formatMoney(this.bank, 2, '.', ',').toString().replace('-', '') + '</span>');
		}
	};

	setBank(money) {
		this.bank += money;
		this.updateBoard();
	};

	flipCards() {
		$('.down').each(function() {
			$(this).removeClass('down').addClass('up');
			renderCard(false, false, false, 0, $(this));
		});

		$('#dcard-0 .popover-content').html(dealer.getScore());
	};

	getScore(){
		return this.handValue
	}
}

var ranks = ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K'];
var suits = ['&#9824;', '&#9827;', '&#9829;', '&#9670;'];

class Card {

	constructor(r,s){
		this.rank = r
		if (s=="s"){
			this.suit = suits[0]
		}else if (s=="c"){
			this.suit = suits[1]
		}else if (s=="h"){
			this.suit = suits[2]
		}else{
			this.suit = suits[3]
		}
	}

	getRank() {
		return this.rank;
	};

	getSuit() {
		return this.suit;
	};

	getValue() {
		var rank  = this.getRank(),
				value = 0;

		if(rank === 'A') {
			value = 11;
		} else if(rank === 'K') {
			value = 10;
		} else if(rank === 'Q') {
			value = 10;
		} else if(rank === 'J') {
			value = 10;
		} else {
			value = parseInt(rank, 0);
		}

		return value;
	};
}

function dealCard(num, i, obj) {

		if(i >= num) { return false; }

		var sender   = obj[i],
			elements = obj[i].getElements(),
			score    = elements.score,
			ele      = elements.ele,
			dhand    = dealer.getHand();

		if(i < 3) {
			renderCard(ele, sender, 'up', i%2);
			$(score).html(sender.getScore());
		} else {
			renderCard(ele, sender, 'down', i%2);
		}

		if(player.getHand().length < 3) {
			if(dhand.length > 0 && dhand[0].rank === 'A') {
				setActions('insurance');
			}
	
			dealer.flipCards();
			$('#dscore span').html(dealer.getScore());

			if(dhand.length > 1) {
				setActions('run');
			}
		}

		function showCards() {
			setTimeout(function() {
				dealCard(num, i + 1, obj);
			}, 500);
		}

		clearTimeout(showCards());
	}



/*****************************************************************/
/************************* Extensions ****************************/
/*****************************************************************/

	Player.prototype.hit = function(dbl) {
		var pscore;

		deal.dealCard(1, 0, [this]);
		pscore = player.getScore();

		if(dbl || pscore > 21) {
			running = false;

			setTimeout(function() {
				player.stand();
			}, 500);
		} else {
			this.getHand();
		}

		setActions();

		player.updateBoard();
	};

	Player.prototype.stand = function() {
		var timeout = 0;

    running = false;
		dealer.flipCards();

		function checkDScore() {
			if(dealer.getScore() < 17 && player.getScore() <= 21) {
				timeout += 200;

				setTimeout(function() {
					dealer.hit();
					checkDScore();
				}, 500);
			} else {
				setTimeout(function() {
					getWinner();
				}, timeout);
			}
		}

		checkDScore();
	};

	Player.prototype.dbl = function() {
		var wager = this.getWager();

		if(this.checkWager(wager * 2)) {
			$('#double').prop('disabled', true);
			this.setWager(wager);
			this.setCash(-wager);
			
			this.hit(true);
		} else {
			$('#alert').removeClass('alert-info alert-success').addClass('alert-error');
			showAlert('You don\'t have enough cash to double down!');
		}
	};

	Player.prototype.split = function() {
		$('#alert').removeClass('alert-info alert-success').addClass('alert-error');
		showAlert('Split function is not yet working.');
	};

	Player.prototype.insure = function() {
		var wager    = this.getWager() / 2,
		  	newWager = 0;

		$('#insurance').prop('disabled', true);
		this.setWager(wager);

		if(this.checkWager()) {
			newWager -= wager;
			this.setCash(newWager);
			insured = wager;
		} else {
			this.setWager(-wager);
			$('#alert').removeClass('alert-info alert-success').addClass('alert-error');
			showAlert('You don\'t have enough for insurance!');
		}
	};

	Player.prototype.updateBoard = function() {
		var score = '#dcard-0 .popover-content';

		if(this === player) {
			score = '#pcard-0 .popover-content';
		}

		$(score).html(this.getScore());
		$('#cash span').html(player.getCash());
		player.getBank();
	};

	function formatMoney(n, c, d, t) {
		var s = n < 0 ? '-' : '',
		    i = parseInt(n = Math.abs(+n || 0).toFixed(c)) + '',
		    j = i.length;
		    j = j > 3 ? j % 3 : 0;
	   return s + (j ? i.substr(0, j) + t : '') + i.substr(j).replace(/(\d{3})(?=\d)/g, '$1' + t) + (c ? d + Math.abs(n - i).toFixed(c).slice(2) : '');
	 };

/*****************************************************************/
/************************** Functions ****************************/
/*****************************************************************/

(function($) {
$.fn.disableSelection = function() {
	return this.attr('unselectable', 'on')
				.css('user-select', 'none')
				.on('selectstart', false);
};
}(jQuery));

(function($) {
	$.fn.numOnly = function() {
		this.on('keydown', function(e) {
			if(e.keyCode === 46 || e.keyCode === 8 || e.keyCode === 9 || e.keyCode === 27 || e.keyCode === 13 || (e.keyCode === 65 && e.ctrlKey === true) || (e.keyCode >= 35 && e.keyCode <= 39)) {
				return true;
			} else {
				if(e.shifKey || ((e.keyCode < 48 || e.keyCode > 57) && (e.keyCode < 96 || e.keyCode > 105))) {
					e.preventDefault();
				}
			}
		});
	};
}(jQuery));

function showAlert(msg) {
	$('#alert span').html('<strong>' + msg + '</strong>');
	$('#alert').fadeIn();
}

function setActions(opts) {
	var hand = player.getHand();
	running = false;

	if(!running) {
		$('#hit')   .prop('disabled', true);
		$('#stand') .prop('disabled', true);
		$('#double').prop('disabled', true);
		$('#split') .prop('disabled', true);
		$('#insurance').prop('disabled', true);
	}

	if(opts === 'run') {
		$('#hit')   .prop('disabled', false);
		$('#stand') .prop('disabled', false);

		if(player.checkWager(wager * 2)) {
			$('#double').prop('disabled', false);
		}
	} else if(opts === 'split') {
		$('#split').prop('disabled', false);
	} else if(opts === 'insurance') {
		$('#insurance').prop('disabled', false);
	} else if(hand.length > 2) {
		$('#double')   .prop('disabled', true);
		$('#split')    .prop('disabled', true);
		$('#insurance').prop('disabled', true);
	}
}

function showBoard() {
	dealCard(4, 0, [player, player, dealer, dealer]);
}


function renderCard(ele, sender, type, i, item) {
	var hand, card;

	if(!item) {
		hand = sender.getHand();
		//i    = hand.length - 1;
		card = hand[i];
	} else {
		hand = dealer.getHand();
		card = hand[1];
	}
	
	var	rank  = card.getRank(),
			suit  = card.getSuit(),
			color = 'red',
			posx  = 402,
			posy  = 182,
			speed = 200,
			cards = ele + ' .card-' + i;
	console.log(i)

	posx -= 50 * i;

	if(!item) {
		$(ele).append(
			'<div class="card-' + i + ' ' + type + '">' + 
				'<span class="pos-0">' +
					'<span class="rank">&nbsp;</span>' +
					'<span class="suit">&nbsp;</span>' +
				'</span>' +
				'<span class="pos-1">' +
					'<span class="rank">&nbsp;</span>' +
					'<span class="suit">&nbsp;</span>' +
				'</span>' +
			'</div>'
		);

		if(ele === '#phand') {
			posy  = 360;
			speed = 500;
			$(ele + ' div.card-' + i).attr('id', 'pcard-' + i);

			if(hand.length < 2) {
				$('#pcard-0').popover({
					animation: false,
					container: '#pcard-0',
					content: player.getScore(),
					placement: 'left',
					title: 'You Have',
					trigger: 'manual'
				});

				setTimeout(function() {
					$('#pcard-0').popover('show');
					$('#pcard-0 .popover').css('display', 'none').fadeIn();
				}, 500);
			}
		} else {
			$(ele + ' div.card-' + i).attr('id', 'dcard-' + i);

			if(hand.length < 2) {
				$('#dcard-0').popover({
					container: '#dcard-0',
					content: dealer.getScore(),
					placement: 'left',
					title: 'Dealer Has',
					trigger: 'manual'
				});

				setTimeout(function() {
					$('#dcard-0').popover('show');
					$('#dcard-0 .popover').fadeIn();
				}, 100);
			}
		}

		$(ele + ' .card-' + i).css('z-index', i);

		console.log(posx)
		$(ele + ' .card-' + i).animate({
			'top': posy,
			'right': posx
		}, speed);

		$(ele).queue(function() {
			$(this).animate({ 'left': '-=25.5px' }, 100);
			$(this).dequeue();
		});
	} else {
		cards = item;
	}

	if(type === 'up' || item) {
		if(suit !== '&#9829;' && suit !== '&#9670;') {
			color = 'black';
		}

		$(cards).find('span[class*="pos"]').addClass(color);
		$(cards).find('span.rank').html(rank);
		$(cards).find('span.suit').html(suit);
	}
}

function resetBoard() {
	$('#dhand').html('');
	$('#phand').html('');
	$('#result').html('');
	$('#phand, #dhand').css('left', 0);
}

function getWinner() {
	var phand    = player.getHand(),
			dhand    = dealer.getHand(),
			pscore   = player.getScore(),
			dscore   = dealer.getScore(),
			wager    = player.getWager(),
			winnings = 0,
			result;

	running = false;
	setActions();

	if(pscore > dscore) {
		if(pscore === 21 && phand.length < 3) {
			winnings = (wager * 2) + (wager / 2);
			player.setCash(winnings);
			player.setBank(winnings - wager);
			$('#alert').removeClass('alert-info alert-error').addClass('alert-success');
			result = 'Blackjack!';
		} else if(pscore <= 21) {
			winnings = wager * 2;
			player.setCash(winnings);
			player.setBank(winnings - wager);
			$('#alert').removeClass('alert-info alert-error').addClass('alert-success');
			result = 'You win!';
		} else if(pscore > 21) {
			winnings -= wager;
			player.setBank(winnings);
			$('#alert').removeClass('alert-info alert-success').addClass('alert-error');
			result = 'Bust';
		}
	} else if(pscore < dscore) {
		if(pscore <= 21 && dscore > 21) {
			winnings = wager * 2;
			player.setCash(winnings);
			player.setBank(winnings - wager);
			$('#alert').removeClass('alert-info alert-error').addClass('alert-success');
			result = 'You win - dealer bust!';
		} else if(dscore <= 21) {
			winnings -= wager;
			player.setBank(winnings);
			$('#alert').removeClass('alert-info alert-success').addClass('alert-error');
			result = 'You lose!';
		}
	} else if(pscore === dscore) {
		if(pscore <= 21) {
			if(dscore === 21 && dhand.length < 3 && phand.length > 2) {
				winnings -= wager;
				player.setBank(winnings);
				$('#alert').removeClass('alert-info alert-success').addClass('alert-error');
				result = 'You lose - dealer Blackjack!';
			} else {
				winnings = wager;
				$('#alert').removeClass('alert-error alert-success').addClass('alert-info');
				player.setCash(winnings);
				result = 'Push';
			}
		} else {
			winnings -= wager;
			player.setBank(winnings);
			$('#alert').removeClass('alert-info alert-success').addClass('alert-error');
			result = 'Bust';
		}
	}

	showAlert(result);

	dealer.flipCards();
	dealer.updateBoard();

	if(parseInt(player.getCash()) < 1) {
		$('#myModal').modal();
		$('#newGame').on('click', function() {
			player.setCash(1000);
			$(this).unbind('click');
			$('#myModal').modal('hide');
		});
	}
}

/*****************************************************************/
/*************************** Actions *****************************/
/*****************************************************************/

$('#hit').on('click', function() {
	socket.emit("game_event",{"pid":player.pid,"type":"hit"});
});

$('#stand').on('click', function() {
	socket.emit("game_event",{"pid":player.pid,"type":"stand"});
});

$('#double').on('click', function() {
	socket.emit("game_event",{"pid":player.pid,"type":"double"});
});

$('#split').on('click', function() {
	socket.emit("game_event",{"pid":player.pid,"type":"split"});
});

$('#insurance').on('click', function() {
	socket.emit("game_event",{"pid":player.pid,"type":"insure"});
});

/*****************************************************************/
/*************************** Loading *****************************/
/*****************************************************************/

$('#wager').numOnly();
$('#actions:not(#wager), #game, #myModal').disableSelection();
$('#newGame, #cancel').on('click', function(e) { e.preventDefault(); });
$('#cancel').on('click', function() { $('#myModal').modal('hide'); });
$('#wager').val(100);

