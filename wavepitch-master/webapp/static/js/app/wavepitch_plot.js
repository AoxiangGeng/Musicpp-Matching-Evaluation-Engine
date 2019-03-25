
define([ 'jquery',  'd3' , 'd3tip'], function($, d3, d3tip) {
	
	function supportsSVG() {
		
	    return !!document.createElementNS && !!document.createElementNS('http://www.w3.org/2000/svg', "svg").createSVGRect;
	    
	  }

	if (!supportsSVG()){
		$("#content_not_supported").show();
		$("#main_content").hide();
		return;
	}


	var dimension = {
			width : 1600,
			height : 600,
			margin : 50
	};

	var svg_chart = d3.select("#wavepitch_chart_container")
	.append("svg")
	.attr("width", dimension.width + 2 * dimension.margin)
	.attr("height", dimension.height + 2 * dimension.margin)
	.append("svg:g").attr("class", "chart").attr("transform",
			"translate(" + dimension.margin + ", " + dimension.margin + ")");
	



	svg_chart.append("svg:g").attr("id", "xaxis").attr("transform",
			"translate(" + 0 + ", " + (dimension.height) + ")");
	svg_chart.append("svg:g").attr("id", "yaxis");






	var tip = d3.tip().attr('class', 'd3-tip');


	var analyse_callback = function(data) {
		/**
		 * data is a JSON containing note_names: array of note names
		 * note_numbers: internal node number, difference in note number denote
		 * difference in semi tone and A(octave 4) = 57, and B(4) = 59 (middle C
		 * is C(octave 4), C(4) = 48) time_values: array of time in seconds
		 * active_notes: array of {n (note_index), t (time_index), v (value of
		 * whether note is active)}
		 * 
		 */
    
		
		// process the data first
		data.active_notes = data.active_notes.map(function(d) {
			d.note_name = data.note_names[d.n];
			d.note_number = data.note_numbers[d.n];
			d.time_value = data.time_values[d.t];
			return d;
		});

		var max_time = (d3.max(data.active_notes, function(note_data){return note_data.time_value;}));
		var min_time = (d3.min(data.active_notes, function(note_data){return note_data.time_value;}));
		var max_note = (d3.max(data.active_notes, function(note_data){return note_data.note_number;}));
		var min_note = (d3.min(data.active_notes, function(note_data){return note_data.note_number;}));
		var max_value = (d3.max(data.active_notes, function(note_data){return note_data.v;}));
		var min_value = (d3.min(data.active_notes, function(note_data){return note_data.v;}));
		var time_delta =  (d3.max(data.time_values) - d3.min(data.time_values))/(data.time_values.length-1);

		 
    var the_width  = Math.max(dimension.width, ((max_time - min_time)/ time_delta + 2) * 10 + 
        2 * dimension.margin);

    d3.select('#wavepitch_chart_container > svg').attr('width', the_width);
		

		var xscale = d3.scale.linear()
		.domain([min_time - time_delta, max_time + time_delta])
		.range([ 0, dimension.width ]);


		var yscale = d3.scale.ordinal()
		.domain(d3.range(min_note, max_note + 1))
		.rangeBands([ dimension.height , 0]);

		var colorScale = d3.scale.pow().exponent(0.25).range(
				[ "#FFFFFF",  "#471807" ]).domain([ 0.001, max_value ]);
		var ydomain = data.note_numbers
		.map(function(d, i){ return [d, data.note_names[i]];})
		.filter(function(d){return d[0] >= min_note && d[0]<= max_note;})
		.map(function(d){return d[1];});
		var yaxis_scale = d3.scale.ordinal()
		.domain(ydomain)
		.rangeBands([ dimension.height , 0]);

		var xaxis = d3.svg.axis().scale(xscale).orient("bottom");
		var yaxis = d3.svg.axis().scale(yaxis_scale).orient("left");

		tip
		.offset([-12, 0])
		.html(function(d) { 
			return  "Time: " + d.time_value + ", Note: " + d.note_name; });


		(d3.select('svg')).call(tip);

		// Display the axes.
		svg_chart.select("#xaxis").call(xaxis);
		svg_chart.select("#yaxis").call(yaxis);


		// Insert the data points.
		var rects = svg_chart.selectAll("rect")
		.data(data.active_notes);
		
		rects.enter().append("rect");
		rects.exit().remove();
		
		rects.attr("x", function(d) { return xscale(d.time_value - time_delta/2.0);})
		.attr("y", function(d) {return yscale(d.note_number );})
		.attr("width", function(d) {return Math.abs(xscale(time_delta) - xscale(0));})
		.attr("height", function(d) {return yscale.rangeBand();})
		.style("fill", function(d) {return colorScale(d.v);})
		// .on("mouseover", tip.show)
		// .on("mouseout", tip.hide)

		.on("mouseover", function() {

			var args = Array.prototype.slice.call(arguments);
			var d = args[0]; 

			d3.select("#wavepitch_note_detail input")
			.property("value", function() {
				if (d.v > 0) {
					return "Time: " + d.time_value + ", Note: " + d.note_name ;
				} else {
					return " ";
				}
			});
			tip.show.apply(this, args);

		})

		.on("mouseout", function() {
			var args = Array.prototype.slice.call(arguments);

			d3.select("#wavepitch_note_detail input")
			.property("value", function() {
				return " ";
			});
			tip.hide.apply(this, args);

		})

		;

		$("#wavepitch_overlay").hide();

	};


	var error_callback = function (jqXHR, exception, _){
		$('#wavepitch_error_box').show();

	} ;

	


	var show_validation = function(ele){
		var val = ele.val();

		if (!(val.indexOf('http://', 0) === 0 || val.indexOf('https://', 0) ===0)){
			ele.parent().addClass('has-warning');
		} else {
			ele.parent().removeClass('has-warning');
		}

	};

	
	var toggle_running_controls = function(is_running){
	  
		$('#wavepitch_analyse input').prop('disabled', is_running);
		$('#wavepitch_analyse button').prop('disabled', is_running);
		if (is_running){
		  $('#wavepitch_overlay').addClass('watchpitch_running');
		  $('#wavepitch_overlay').removeClass('watchpitch_not_running');
		}
		else{
		  $('#wavepitch_overlay').removeClass('watchpitch_running');
		  $('#wavepitch_overlay').addClass('watchpitch_not_running');
		}
		
	};
	
	var complete_callback = function(){
		toggle_running_controls(false);
    
	};

  var run_analyse = function(filtered){
    console.log('here');
    $("#wavepitch_overlay").show();
      $('#wavepitch_error_box').hide();
      toggle_running_controls(true);
      $.ajax({
        url : "/analyse/",
        type : 'POST',
        data : {
          url : $("#wavepitch_analyse input").val(),
          filtered: filtered
        },
        dataType : "json",
        success : analyse_callback,
        error: error_callback,
        complete: complete_callback
      });
    
    
  };


	$(function() {

    toggle_running_controls(false);
		$( window ).resize(function() {
			$("#wavepitch_overlay")
			.width($("#wavepitch_overlay").parent().width())
			.height($("#wavepitch_overlay").parent().height());
		});  

		$("#wavepitch_overlay")
		.width($("#wavepitch_overlay").parent().width())
		.height($("#wavepitch_overlay").parent().height());

		$('#wavepitch_error_box').hide();



		$('#wavepitch_error_box .close').on('click', function(e) {
			$(this).parent().hide();
		});


		$("#wavepitch_analyse #wavepitch_main_button").click(function() {
      run_analyse(true);
			
		});

    $("#wavepitch_analyse #wavepitch_filtered_button").click(function() {
      run_analyse(true);
      
    });
    
    $("#wavepitch_analyse #wavepitch_full_button").click(function() {
      run_analyse(false);
      
    });

		$('#wavepitch_analyse input').keyup(function(e){

			show_validation($(this));
		});




    console.log('end setup');
	});


});