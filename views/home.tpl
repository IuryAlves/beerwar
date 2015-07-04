<html>
	<head>
		<script src="/assets/jquery-1.3.2.min.js"></script>
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
						  j = JSON.parse(r);
						  var w = j.length;
						  for(var i = 0; i<=w;i++){
						    // tr
						    x = j[i];
						    tr = $('<tr>').appendTo(matrix);
		                                    var e = x.length;
						    for(var n = 0; n<=e;n++){
							// td
							    tr.append($("<td>").html(x[n]));
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
