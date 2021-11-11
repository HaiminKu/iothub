/* Show hidden filters by clicking "Filter" button on the monitor.html*/
$(document).ready(function(){
  // If a user clicks button tag right under #filter
  $("#filter>button").click(function(){
    $(this).next("table").toggleClass("hide");
  });

/* Filter function*/
  $("#filter-form button").click(function(ev){
    ev.preventDefault()// cancel form submission
    var value = $(this).attr("value")
    switch(value) {
      case "btn-hide":
        $(this).next("div").toggleClass("hide");
        break;
      case "btn-apply":
        var type = $("#dropdown option:selected").val() + "_" + $("input[name=chk_info]:checked", "#filter-form").val();
        reset();
        form_action(type);
        break;
      case "btn-reset":
        reset();
        window.location.reload();
        break
      default:
        break;
    }
  });

  $("#filter-form").click(function(){
  });

});

function draw_graph(type, path) {
  $.ajax({
    dataType: "json",
	url: path,
	success: (result) => {
	  drawBar(type, result.data, "rgba(200,0,0,0.2)");
	  drawPie(type, result.data, "rgba(200,0,0,0.2)");
	  drawLine(type, result.data, "rgba(200,0,0,0.2)");
	  }
	})
}

/* Make graphs */
function form_action(type){
  console.log(type);
  var timeUnit = type.split("_");

  switch(timeUnit[0]) {
    case "Temperature":
	  draw_graph(timeUnit[0], "/static/hubapp/data_temp.json");
      break;
    case "Humidity":
	  draw_graph(timeUnit[0], "/static/hubapp/data_humid.json");
      break;
    case "Optic":
	  draw_graph(timeUnit[0], "/static/hubapp/data_optic.json");
      break;
    case "Proximity":
	  draw_graph(timeUnit[0], "/static/hubapp/data_prox.json");
      break;
    case "Relay-Module":
	  draw_graph(timeUnit[0], "/static/hubapp/data_relay.json");
      break;
  }
}
function drawBar(type, data, graph_color){
  var canvas = document.getElementById("barCanvas");
  var ctx = canvas.getContext("2d");
  var width= 10;  // bar width

  for (var i = 0; i < data.length; i ++) {
    var x = i * 20;
    var y = data[i].val;
    ctx.fillStyle = graph_color
    ctx.fillRect(x, canvas.height - 20 - y, width, y);

    // show bar number
    ctx.fillStyle = "rgba(100,100,100)";
    ctx.fillText(y, x, canvas.height - 20 - y -10);
    ctx.fillText(i, x, canvas.height - 10);
  }
  ctx.fillText(type, canvas.width/2, 10)
}

function drawPie(type, data, graph_color) {
  var canvas = document.getElementById("pieCanvas");
  var ctx = canvas.getContext("2d");

  var center_x = canvas.width / 2;
  var center_y = canvas.height / 2;

  ctx.fillStyle = "#00ff00";
  ctx.beginPath();
  ctx.moveTo(center_x,center_y);
  ctx.arc(center_x,center_y,center_y - 20, 0 * Math.PI/180, 60 * Math.PI/180, false); //x, y, 반지름, 시작점, 끝점, 그리는 방향
  ctx.closePath();
  ctx.fill();

  ctx.fillStyle = "#ff0000";
  ctx.beginPath();
  ctx.moveTo(center_x,center_y);
  ctx.arc(center_x,center_y,center_y - 20, 60 * Math.PI/180, 120 * Math.PI/180, false); //x, y, 반지름, 시작점, 끝점, 그리는 방향
  ctx.closePath();
  ctx.fill();

  ctx.fillStyle = "#0000ff";
  ctx.beginPath();
  ctx.moveTo(center_x,center_y);
  ctx.arc(center_x,center_y,center_y - 20, 100 * Math.PI/180, 240 * Math.PI/180, false); //x, y, 반지름, 시작점, 끝점, 그리는 방향
  ctx.closePath();
  ctx.fill();

  ctx.fillStyle = "#ffff00";
  ctx.beginPath();
  ctx.moveTo(center_x,center_y);
  ctx.arc(center_x,center_y,center_y - 20, 240 * Math.PI/180, 360 * Math.PI/180, false); //x, y, 반지름, 시작점, 끝점, 그리는 방향
  ctx.closePath();
  ctx.fill();
}

function drawLine(type, data, graph_color) {
  const canvas = document.getElementById("lineCanvas");
  const ctx = canvas.getContext("2d");

  const pad = 10;
  const chartInnerWidth = canvas.width - 2 * pad;
  const chartInnerHeight = canvas.height - 2 * pad;

  ctx.moveTo(pad, pad);
  ctx.lineTo(pad, pad + chartInnerHeight);
  ctx.stroke();

  ctx.moveTo(pad, pad + chartInnerHeight);
  ctx.lineTo(pad + chartInnerWidth, pad + chartInnerHeight);
  ctx.stroke();

  var x = pad;
  var y = data[0].val;
  ctx.moveTo(pad, chartInnerHeight - y);
  console.log("x:", x, "y:", y);

  for (var i = 1; i < data.length; i++) {
    x += 20;
    y = data[i].val;

    ctx.lineTo(x, chartInnerHeight - y);
    ctx.fillStyle = "rgba(100,100,100)";
    ctx.fillText(y, x, chartInnerHeight - y - 10);
  }
  ctx.stroke();
}

function reset(){
  // Clearing the Canvas
  var canvas = document.getElementById("lineCanvas");
  var ctx = canvas.getContext("2d");
  ctx.clearRect(0, 0, canvas.width, canvas.height);

  var canvas = document.getElementById("barCanvas");
  var ctx = canvas.getContext("2d");
  ctx.clearRect(0, 0, canvas.width, canvas.height);

  var canvas = document.getElementById("pieCanvas");
  var ctx = canvas.getContext("2d");
  ctx.clearRect(0, 0, canvas.width, canvas.height);
}
