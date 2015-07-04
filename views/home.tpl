<html>
	<head>
		<script src="/assets/jquery-1.3.2.min.js"></script>
		<style>
		#matrix {
			background-image: url(/assets/images/bg.jpg);
			border-spacing: 0;
			border-collapse: collapse;
		}
		#matrix td {
			width: 60px;
			height: 60px;
			text-align: center;
			vertical-align: bottom;
			color: #ffffff;
		}
		#matrix td.tank {
			background-image: url(/assets/images/tanque.png);
		}
		#matrix td.barrier {
			background-image: url(/assets/images/barrier.png);
		}

		</style>
	</head>
	<body>
		<table id="matrix"></table>
		<script>
			$(document).ready(function() {
				var ajax = function() {

					$.ajax({
					  url: "/matrix/",
					  success: function(r){
						  matrix = $("#matrix");
						  matrix.html("");
						  tdclass = '';
						  j = JSON.parse(r);
						  var w = j.length;
						  for(var i = 0; i<=w;i++){
						    // tr
						    x = j[i];
						    tr = $('<tr>').appendTo(matrix);
		                                    var e = x.length;
						    for(var n = 0; n<=e;n++){
							// td
							    if(x[n] == '_') {
							    	tdclass = '';
							    	text = '&nbsp;';
							    } else if(x[n] == '#'){
							    	tdclass = 'barrier';
							    	text = '&nbsp;';
							    } else {
							    	tdclass = 'tank';
							    	text = x[n];
							    }

							    tr.append($('<td class="' + tdclass + '">').html(text));
							}
						  }
					  }
					})
				};
				ajax();
				setInterval(ajax, 1000);
			});
		</script>
	</body>
</html>     
