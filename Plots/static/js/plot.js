var lineChart = null;
//var color = 'rgba(255, 255, 255, 0.2)';

/*Chart.defaults.global.defaultFontFamily = "Lato";
Chart.defaults.global.defaultFontSize = 15;*/

//TODO:Нельзя нажать save пока не нажата caclculate 
//TODO:Нельзя нажать save если график не изменился
//TODO:Нельзя нажать save если изменились входные данные

class PlotInfo {
	constructor(equation, step, left, right){
		this.equation = equation;
		this.step = step;
		this.left = left;
		this.right = right;
	}
}
var object = null;
function ChangeColor(){
	var colorBack = 'rgba('+Math.random()*255+','+Math.random()*255+','+Math.random()*255+','+0.2+')';
	var colorPBorder = 'rgba('+Math.random()*255+','+Math.random()*255+','+Math.random()*255+','+0.2+')';
	var colorPBack = 'rgba('+Math.random()*255+','+Math.random()*255+','+Math.random()*255+','+0.2+')';
	lineChart.data.datasets[0].backgroundColor = colorBack;
	lineChart.data.datasets[0].pointBorderColor = colorPBorder;
	lineChart.data.datasets[0].pointBackgroundColor = colorPBack; 
	lineChart.update();
}
function drawPlot(new_data,left,right,labelValues,equation=1,color = 'rgba(255, 255, 255, 0.2)'){
	var speedCanvas = document.getElementById("speedChart");
	var speedData = {
	labels:labelValues,
	datasets: [
	{	
		label: equation,
		backgroundColor: color,
		pointBorderColor: 'rgb(28,29,34)',
		pointBackgroundColor: 'rgb(12,91,125)',
		}
	]
	};

	var chartOptions = {
		tooltips: {
		enabled: true,
		mode: 'label',
		
		
 },
	legend: {
		display: true,
		position: 'top',
		onClick: function(element,dataAtClick){
			alert(element,dataAtClick);
		},
		labels: {
			boxWidth: 80,
			fontColor: 'black'
		}
	},
	
		title:{
			display:true,
			text:'Plot'
			
			},
		
		scales:{
			xAxes:[{
				ticks:{
					min:left,
					max:right,
					stepSize:1,
				},
			
			}],
			yAxes:[{
				gridLines:{
					offsetGridLines:true
				}
			}]
			
		}
	}
	addData(speedData,new_data);
	lineChart = new Chart(speedCanvas, {
		type: 'line',
		data: speedData,
		options: chartOptions,
	});
	lineChart.update();	
} 
function checkDiapason(left,right,step){
	left = parseInt(left);
	right = parseInt(right);
	step = parseFloat(step);
	var result = 0;
	if(step < 0){
		alert("Step less than zero");
		return false;
	}else if(right<left){
		alert("Right value less than left");
		return false;
	}else{
		result = left+(400 - 1)*step
		if(result+1 < right){
			alert("More than 400 points in this range");
			return false;
		}else{
			return true;
		}
	}
}
function compare_usr_data(data,left,right,step){
	var result_d = data.localeCompare(object.equation) +
				   left.localeCompare(object.left) + right.localeCompare(object.right) + 
				   step.localeCompare(object.step);
	return result_d;
}
function send_data(){
  var data = document.getElementById("equation").value;
  var left = document.getElementById("diapasonLeft").value;
  var right = document.getElementById("diapasonRight").value;
  var step = document.getElementById("step").value;
  if(step == ''){step = '0.1';}
  if(left == ''){left = '0';}
  if(right == ''){right = '5';}
  if(object != null){
		var result = compare_usr_data(data,left,right,step);
		if (result == 0){
			alert("This equation is already calculated");
			return 0;
		}
  }
  var flag = checkDiapason(left,right,step)
  if(flag == true){
	object = new PlotInfo(data,step,left,right);
	
  	$.ajax({
    	type:"POST",
    	url:"calc/",
    	data:{
      	'equation':data,
	  	'left':left,
	  	'right':right,
	  	'step':step,
    	},
    	dataType:"text",
    	success: function (response) {
	  	var title;
      	var json = JSON.parse(response);
	  	if(json.status!=""){
			alert(json.status);
			object = null;
	  	} else{
			lineChart.destroy()
			var new_data = json.values;

			var new_data_x = json.values_x;

			title = equTitleFormat(data);
			//labeValues = labelFormat(left,right,step);
			labeValues = labelFormat(new_data_x);
			drawPlot(new_data,left,right,labeValues,title);
			step = 0;
	  			}    
    		}
  		})
	}
}
/*function labelFormat(left,right,step){
	if(!(left && right &&step)){
		left = 0;
		right = 5;
		step = 0.1;
	}
	 var labelV = [];
	 step = parseFloat(step)
	 step = parseFloat(parseFloat(step).toFixed(1));
	 left = parseFloat(left);
	 right = parseFloat(right);
	 while(left<=right){
		labelV.push(left.toFixed(1));
        left+=step;
	  }
	return labelV;
}*/

function labelFormat(new_data_x){
	 var labelV = [];
	  new_data_x.forEach(function(entry){
		entry = parseFloat(entry);
		labelV.push(entry.toFixed(1))
	  });
	return labelV;
}

function equTitleFormat(equation){
	var new_title;
	var symbols = ['+','/','*','-',')',']']
	for(var i = 0;i<equation.length;i++){
		if(symbols.indexOf(equation[i]) != -1 || i == equation.length-1){
			if(i<10){
				new_title = equation.slice(0,i+1);
				
			} else{
				new_title = equation.slice(0,i+1) + "...";
				return new_title;
			}
		}
	}
	return new_title;
}

function addData(lineChart,data){
	lineChart.datasets[0].data = data;
	  }

if(window.location.pathname == '/'){
	drawPlot();
}

function fillCanvas(color = 'white'){
	var canvas = document.getElementById('speedChart');
	var context = canvas.getContext('2d');
	context.save();
	context.globalCompositeOperation = 'destination-over';
	context.fillStyle = color;
	context.fillRect(0,0,canvas.width,canvas.height);
	context.restore();
}

function create_str_interval(left, right){
	if(left == ''){
		left = '0';
	}
	if(right == ''){
		right = '5';
	}
	var new_str = "from " + left + " to " + right;
	return new_str;
}

function save(){
	fillCanvas('#1c1d22');
	if(object == null){alert('Вы кое-что забыли!');return 0;}
	var equation = object.equation;
	var left = object.left;
	var right = object.right;
	var step = object.step;
	var interval = create_str_interval(left, right);
	var url = lineChart.toBase64Image();
	$.ajax({
		type:"POST",
		url:"save/",
		data:{
		  'url':url,
		  'function':equation,
		  'interval':interval,
		  'step': step,
		},
		dataType:"text",
		success: function (response) {
			var json = JSON.parse(response);
			if(json.status=="ok"){
				url = ''; 
			} else{
				alert(json.status);
			}
		}
	})
}
$(document).ready(function(){
	var modal = document.getElementById('popup1');
	var btnopen = document.getElementById('openmodal');
	var btnclose = document.getElementById('hide'); 
	btnopen.onclick = function(){
		modal.style.display = "block";
	}
	btnclose.onclick = function(){
		modal.style.display = "none";
	}
	window.onclick = function(event){
		if(event.target == modal){
			modal.style.display = "none";
		}
	}
});

