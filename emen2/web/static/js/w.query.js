(function($) {
    $.widget("ui.QueryControl", {
		options: {
			q: null,
			show: true,
			plot: false,
			cb: function(self, q){}
		},
				
		_create: function() {
			if (this.options.show) {
				this.build();
			}
		},
		
		
		build: function() {
			var self = this;
			this.container = $('<div class="query clearfix" />')
			var m = $(' \
				<h4>Keywords</h4> \
				<input type="text" name="q" /> \
				<h4>General</h4> \
				<table><tr> \
					<td>Protocol:</td><td><input type="text" name="rectype" /> <img  class="listicon" data-clear="rectype" src="'+EMEN2WEBROOT+'/images/remove_small.png" /></td> \
					<td>Creator:</td><td><input type="text" name="creator" /> <img  class="listicon" data-clear="creator" src="'+EMEN2WEBROOT+'/images/remove_small.png" /></td> \
				</tr><tr> \
					<td>Child of</td><td><input type="text" name="parent" />  <img  class="listicon" data-clear="parent" src="'+EMEN2WEBROOT+'/images/remove_small.png" /></td> \
					<td>Parent of</td><td><input type="text" name="child" /> <img  class="listicon" data-clear="child" src="'+EMEN2WEBROOT+'/images/remove_small.png" /></td> \
				</tr></table> \
				<table class="constraints"> \
					<thead><tr><th>Parameter</th><th>Operator</th><th>Value</th><th>Child Params</th><th>Search Parents</th><th /></tr></thead> \
					<tbody></tbody> \
				</table> \
				<h4>Options</h4> \
				<p>Match \
					<input type="radio" value="AND" name="boolmode" checked="checked"> all <input type="radio" value="OR" name="boolmode"> any \
					<input type="checkbox" checked="checked" name="ignorecase" /> Case Insensitive \
					<input type="checkbox" name="recurse" /> Recursive</p> \
				');
			this.container.append(m);

			var plot = $(' \
				<h4>Plot</h4> \
				<table cellpadding="0" cellspacing="0"> \
					<thead><th /><th>Param</th><th>Min</th><th>Max</th></tr></thead> \
					<tbody> \
						<tr><td>X</td><td><input type="text" name="xparam" /></td><td><input type="text" name="xmin" /></td><td><input type="text" name="xmax" /></td></tr> \
						<tr><td>Y</td><td><input type="text" name="yparam" /></td><td><input type="text" name="ymin" /></td><td><input type="text" name="ymax" /></td></tr> \
					</tbody> \
				</table> \
				<p>Output: <input type="checkbox" name="png" /> PNG <input type="checkbox" name="pdf" /> PDF <input type="text" name="width" value="800" /> Pixels </p> \
			');
			
			if (this.options.plot) {
				this.container.append(plot);
			}

			this.container.append('<div class="controls"><input type="button" value="Query" name="update" /></div>');

			$('input[name=rectype]', this.container).FindControl({mode: 'findrecorddef'});			
			$('input[name=creator]', this.container).FindControl({mode: 'finduser'});
			$('input[name=parent]', this.container).Browser({});
			$('input[name=child]', this.container).Browser({});
			$('input[name=update]', this.container).click(function() {self.query()});
			$('.listicon', this.container).click(function() {
				var clearselector = $(this).attr('data-clear');
				$('input[name='+clearselector+']').val('');
			});
			
			this.element.append(this.container);
			
			this.update();
		},
		
		query: function() {
			var self = this;
			var newq = {};
			var constraints = [];

			var ignorecase = $('input[name=ignorecase]', this.container).attr('checked');
			var recurse = $('input[name=recurse]', this.container).attr('checked');
			var boolmode = $('input[name=boolmode]:checked', this.container).val();

			var rectype = $('input[name=rectype]', this.container).val();
			if (rectype) {constraints.push(['rectype', '==', rectype])}

			var creator = $('input[name=creator]', this.container).val();
			if (creator) {constraints.push(['creator', '==', creator])}

			var parent = $('input[name=parent]', this.container).val();
			if (parent) {constraints.push(['parent', 'recid', parseInt(parent)])}

			var child = $('input[name=child]', this.container).val();
			if (child) {constraints.push(['child', 'recid', parseInt(child)])}
						
			$('.constraints .constraint', this.container).each(function() {
				var param = $('input[name=param]', this).val();
				var cmp = $('select[name=cmp]', this).val();
				var value = $('input[name=value]', this).val();
				var childparams = $('input[name=childparams]', this).attr('checked');
				var parents = $('input[name=parents]', this).attr('checked');
				if (param && childparams) {param = param+'*'}
				if (param && parents) {param = param+'^'}
				if (param && cmp) { constraints.push([param, cmp, value]) }
			});
			
			newq['constraints'] = constraints;
			if (ignorecase) {newq['ignorecase'] = true}
			if (recurse) {newq['recurse'] = -1}			
			if (boolmode) {newq['boolmode'] = boolmode}
			
			// $.ajax({
			// 	type: 'POST',
			// 	url: EMEN2WEBROOT+'/db/table/',
			//     data: {"args___json":$.toJSON(newq)},
			// 	success: function(data) {$('.table').html(data)}
			// });			
			this.options.cb(this, newq);

		},
		
		addconstraint: function(param, cmp, value) {
			param = param || '';
			cmp = cmp || '';
			value = value || '';
			var childparams = false;
			var parents = false;
			var self = this;
			var cmpi = this.build_cmp(cmp);

			if (param.indexOf('*') != -1) {
				param = param.replace('*', '');
				childparams = true;
			}	
			
			if (param.indexOf('^') != -1) {
				param = param.replace('^', '');
				parents = true;
			}	

			var newconstraint = $('<tr class="constraint">')
				.append('<td><input type="text" name="param" value="'+param+'" size="15" /></td>')
				.append($('<td/>').append(cmpi))
				.append('<td><input type="text" name="value" value="'+value+'" size="10"  /></td>')
				.append('<td><input name="childparams" type="checkbox" />')
				.append('<td><input name="parents" type="checkbox" />');

			if (childparams) {$('input[name=childparams]', newconstraint).attr('checked', 'checked')}
			if (parents) {$('input[name=parents]', newconstraint).attr('checked', 'checked')}

			var controls = $('<td />');

			var addimg = $('<img class="listicon" src="'+EMEN2WEBROOT+'/images/add_small.png" />');
			addimg.click(function() {self.addconstraint()});

			var removeimg = $('<img  class="listicon" src="'+EMEN2WEBROOT+'/images/remove_small.png" />');
			removeimg.click(function() {
				if ($('.constraints .constraint', self.element).length > 1) {$(this).parent().parent().remove()}
			});

			controls.append(addimg, removeimg);
			newconstraint.append(controls);
			$('input[name=param]', newconstraint).FindControl({mode: 'findparamdef'});
			$('.constraints', this.container).append(newconstraint);
		},
		
		build_cmp: function(cmp) {
			var comparators = {
				"==":"is",
				"!=":"is not",
				"contains":"contains",
				"!contains":"does not contain",
				">":"is greater than",
				"<":"is less than",
				">=":"is greater or equal than",
				"<=":"is less or equal than",
				"!None":"is any value"
			}
			var i = $('<select name="cmp" />');
			$.each(comparators, function(k,v) {
				var r = $('<option value="'+k+'">'+v+'</option>');
				if (cmp==k) {r.attr("selected", "selected")}
				i.append(r);
			});
			return i		
		},
		
		update: function(q) {
			q = q || this.options.q;
			this.options.q = q;
			
			var self = this;
			$('.constraints tbody', this.container).empty();
			$('input[name=q]').val(this.options.q['q']);

			$.each(this.options.q['constraints'], function() {
				if (this[0] == 'rectype' && this[1] == '==') { $('input[name=rectype]', self.container).val(this[2]) }
				else if (this[0] == 'creator' && this[1] == 'recid') { $('input[name=creator]', self.container).val(this[2]) }
				else if (this[0] == 'parent' && this[1] == 'recid') { $('input[name=parent]', self.container).val(this[2]) }
				else {
					self.addconstraint(this[0], this[1], this[2]);
				}
			});
			this.addconstraint();
			if (this.options.q['ignorecase']) {$('input[name=ignorecase]', this.container).attr('checked', 'checked')}
			if (this.options.q['recurse'] == -1) {$('input[name=recurse]', this.container).attr('checked', 'checked')}
			
		},		
				
		destroy: function() {
		},
		
		_setOption: function(option, value) {
			$.Widget.prototype._setOption.apply( this, arguments );
		}
	});
})(jQuery);