(function($) {
    $.widget("emen2.TableControl", {
		options: {
			q: null,
			qc: true,
			create: null,
			parent: null
		},
				
		_create: function() {
			this.build();
		},
		
		build: function() {
			var self = this;

			// Build control elements
			// Record count
			var length = $('<li class="e2-table-length" />');
						
			// Row count
			var count = $('<select name="count" class="small"></select>');
			count.append('<option value="">Rows</option>');
			$.each([1, 10,50,100,500,1000], function() {
				count.append('<option value="'+this+'">'+this+'</option>');
			});
			count.change(function() {
				self.options.q['pos'] = 0;
				self.query();
			})			
			count = $('<li class="e2l-float-right" />').append(count);

			// Page controls			
			var pages = $('<li class="e2l-float-right e2-table-pages"></li>');

			// Activity spinner
			var spinner = $('<li class="e2l-float-right"><img class="e2l-spinner hide" src="'+EMEN2WEBROOT+'/static/images/spinner.gif" alt="Loading" /></li>');

			// Create a new child record
			var create = "";
			if (this.options.rectype && this.options.parent != null) {
				var create = $('<li class="e2l-float-right"><input class="small" data-action="reload" data-rectype="'+this.options.rectype+'" data-parent="'+this.options.parent+'" type="submit" value="New '+this.options.rectype+'" /></li>');
				$('input', create).NewRecordControl({});
			}

			// Add basic controls
			$('.e2-table-header', this.element).append(create, length, pages, count, create, spinner);

			// Kindof hacky..
			this.build_querycontrol();
			this.build_stats();
			this.build_plot();
			this.build_tools();
						
			// Set the control values from the current query state
			this.update_controls();

			// Rebind to table header controls
			this.rebuild_thead();
		},
		
		build_tools: function() {
			// Build the Tools & Statistics menu
			var self = this;
			var q = $('<li><span class="clickable label">Tools<img src="'+EMEN2WEBROOT+'/static/images/caret_small.png" alt="^" /></span></li>');
			var hidden = $('<div class="e2l-menu-hidden"><ul class="e2l-nonlist"> \
						<li class="clickable e2-table-files"><img src="'+EMEN2WEBROOT+'/static/images/action.png" alt="Action" /> Download all files in this table</li> \
					</ul></div>');

			$('.e2-table-files', hidden).click(function() {self.query_download()});
			// $('.e2-batch-edit', hidden).click(function() {self.query_batch_edit()});

			q.append(hidden);
			q.EditbarControl({
				width: 300
			});
			$('.e2-table-header', this.element).append(q);			
		},
		
		build_plot: function() {
			// var self = this;
			// var q = $('<li><span class="clickable label">Plots <img src="'+EMEN2WEBROOT+'/static/images/caret_small.png" alt="^" /></span></li>');
			// var hidden = $('<div class="hidden">Plotting...</div>');
			// q.append(hidden);
			// q.EditbarControl({
			// 	width: 300
			// });
			// $('.e2-table-header', this.element).append(q);			
		},
		
		build_stats: function() {
			var self = this;
			var q = $('<li><span class="clickable label">Statistics<img src="'+EMEN2WEBROOT+'/static/images/caret_small.png" alt="^" /></span></li>');
			var hidden = $('<div class="e2l-menu-hidden"><img class="e2l-spinner" src="'+EMEN2WEBROOT+'/static/images/spinner.gif" alt="Loading" /></div>');
			q.append(hidden);
			q.EditbarControl({
				width: 300
			});				
			$('.e2-table-header', this.element).append(q);						
		},
		
		build_querycontrol: function() {
			// Build the Query control
			if (!this.options.qc) {return}
			
			var self = this;
			var q = $('<li><span class="clickable label"> \
				Query <img src="'+EMEN2WEBROOT+'/static/images/caret_small.png" alt="^" /></span></li>');

			q.EditbarControl({
				width: 700,
				cb: function(self2) {
					self2.popup.QueryControl({
						q: self.options.q,
						keywords: false,
						cb: function(test, newq) {self.query(newq)} 
					});
				}
			});
			$('.e2-table-header', this.element).append(q);
			
		},
		
		query_download: function() {
			// Get all the binaries in this table, and prepare a download link.
			var newq = {};
			newq['c'] = this.options.q['c'];
			newq['boolmode'] = this.options.q['boolmode'];
			newq['ignorecase'] = this.options.q['ignorecase'];
			window.location = query_build_path(newq, 'files');
		},
		
		query_batch_edit: function() {
			alert("Still being implemented..");
			return			
		},
		
		query: function(newq) {
			// Update the query from the current settings
			newq = newq || this.options.q;
			$('.e2-table-header .e2l-spinner', this.element).show();
			var self = this;
			var count = $('.e2-table-header select[name=count]').val();
			if (count) {newq["count"] = parseInt(count)}
			newq['names'] = [];
			newq['recs'] = true;
			newq['table'] = true;
			$.jsonRPC.call("query", newq, function(q){self.update(q)});			
		},
		
		setpos: function(pos) {
			// Change the page
			if (pos == this.options.q['pos']) {return}
			var self = this;
			this.options.q['pos'] = pos;
			this.query();
		},
		
		resort: function(sortkey, args) {
			// Sort by a column key
			if (args) {
				sortkey = '$@' + sortkey + "(" + args + ")"
			}
			if (this.options.q['sortkey'] == sortkey) {
				this.options.q['reverse'] = (this.options.q['reverse']) ? false : true;
			} else {
				this.options.q['reverse'] = false;
			}
			this.options.q['sortkey'] = sortkey;
			this.query();			
		},
		
		update: function(q) {
			// Callback from a query; Update the table and all controls
			this.options.q = q;
			$('.e2-table-header .e2-query-control').QueryControl('update', this.options.q)					
			this.update_controls();
			this.rebuild_table();
			this.options.q['stats'] = true;
			$('.e2-table-header .e2l-spinner', this.element).hide();					
		},	
		
		update_controls: function() {
			// Update the table controls
			var self = this;

			// Update the title bar information
			var title = '';
			var rtkeys = [];
			for (i in this.options.q['stats']['rectypes']) {
				rtkeys.push(i);
			}
			rtkeys.sort();
			
			title = this.options.q['length'] + ' records, ' + rtkeys.length + ' protocols';
			if (rtkeys.length == 0) {
				title = this.options.q['length'] + ' records';				
			} else if (rtkeys.length == 1) {
				title = this.options.q['length'] + ' ' + rtkeys[0] + ' records';
			} else if (rtkeys.length <= 5) {				
				title = title + ": ";
				for (var i=0;i<rtkeys.length;i++) {
					title = title + self.options.q['stats']['rectypes'][rtkeys[i]] + ' ' + rtkeys[i];
					if (i+1<rtkeys.length) {
						title = title + ', ';
					}
				}
			}			

			if (this.options.q['stats']['time']) {
				title = title + ' ('+this.options.q['stats']['time'].toFixed(2)+'s)';
			}

			$('.e2-table-header .e2-table-length').empty();
			$('.e2-table-header .e2-table-length').append('<span class="label">'+title+'</span>');
			
			// Update the record type statistics
			var qstats = $(".e2-query-stats", this.element);
			if (qstats) {
				qstats.empty();
				var t = $('<table><thead><tr><th>Protocol</th><th>Count</th></tr></thead><tbody></tbody></table>');
				for (var i=0;i<rtkeys.length;i++) {
					var tr = $('<tr><td>'+rtkeys[i]+'</td><td>'+self.options.q['stats']['rectypes'][rtkeys[i]]+'</td></td>');
					$('tbody', t).append(tr);
				}
				qstats.append(t);
			}
			
			// Update the page count
			var pages = $('.e2-table-header .e2-table-pages');
			pages.empty();
			var pc = $('<span></span>');
			
			var count = this.options.q['count'];
			var l = this.options.q['length'];
			if (count == 0 || count > l || l == 0) {
				//pages.append("All Records");
			} else {			
				var current = (this.options.q['pos'] / this.options.q['count']);
				var pagecount = Math.ceil(this.options.q['length'] / this.options.q['count'])-1;
				var setpos = function() {self.setpos(parseInt($(this).attr('data-pos')))}			

				var p1 = $('<span data-pos="0" class="clickable">&laquo;</span>').click(setpos);
				var p2 = $('<span data-pos="'+(this.options.q['pos'] - this.options.q['count'])+'" class="clickable">&lsaquo;</span>').click(setpos);
				var p  = $('<span class="label"> '+(current+1)+' / '+(pagecount+1)+' </span>');
				var p3 = $('<span data-pos="'+(this.options.q['pos'] + this.options.q['count'])+'" class="clickable">&rsaquo;</span>').click(setpos);
				var p4 = $('<span data-pos="'+(pagecount*this.options.q['count'])+'" class="clickable">&raquo;</span>').click(setpos);

				if (current > 0) {pc.prepend(p2)}
				if (current > 1) {pc.prepend(p1, '')}
				pc.append(p);
				if (current < pagecount) {pc.append(p3)}
				if (current < pagecount - 1) {pc.append('', p4)}
				pages.append(pc);
			}
		},
				
		
		rebuild_table: function() {
			// Rebuild everything
			this.rebuild_thead();
			this.rebuild_tbody();
		},
				
		rebuild_thead: function() {
			// Rebuild the table header after each update			

			var self = this;
			var t = $('.e2-table-inner', this.element);
			$('thead', t).empty();
			var headers = this.options.q['table']['headers']['null'];
			
			// ian: todo: critical: Properly get immutable parameters.
			var immutable = ["creator","creationtime","modifyuser","modifytime","history","name","rectype","keytype","parents","children"];
			
			var tr = $('<tr />');
			var tr2 = $('<tr />');
			$.each(headers, function() {
				if (this[3] == null) {
					this[3]=''
				}
				var iw = $('<th>'+this[0]+'</th>');
				var bw = $('<th data-name="'+this[2]+'" data-args="'+this[3]+'" ></th>');			

				// An editable, sortable field..
				if (this[1] == "$" && $.inArray(this[2],immutable)==-1) {
					var editable = $('<button name="edit" class="e2l-float-right"><img src="'+EMEN2WEBROOT+'/static/images/edit.png" alt="Edit" /></button>');
					bw.append(editable);
				}

				var direction = 'able';
				if (self.options.q['sortkey'] == this[2] || self.options.q['sortkey'] == '$@'+this[2]+'('+this[3]+')') {
					var direction = 1;
					if (self.options.q['reverse']) {direction = 0}
				}
				
				var sortable = $('<button name="sort" class="e2l-float-right"><img src="'+EMEN2WEBROOT+'/static/images/sort_'+direction+'.png" alt="'+direction+'" /></button>');
				bw.append(sortable);				

				tr.append(iw);
				tr2.append(bw);
			});

			$('button[name=sort]', tr2).click(function(){self.resort($(this).parent().attr('data-name'), $(this).parent().attr('data-args'))});
			$('button[name=edit]', tr2).click(function(e){self.event_edit(e)});						
			$('thead', t).append(tr, tr2);
		},
		
		
		rebuild_tbody: function() {
			// Rebuild the table body
			var self = this;
			var t = $('.e2-table-inner', this.element);			
			var headers = this.options.q['table']['headers']['null'];
			var names = this.options.q['names'];
			var rows = []			
			// if (names.length == 0) {
			// 	var row = '<tr><td colspan="0">No Records found for this query.</td</tr>';
			// 	rows.push(row);
			// }
			console.log(names.length);
			for (var i=0;i<names.length;i++) {
				var row = [];
				for (var j=0;j<headers.length;j++) {
					//row.push('<td>'+self.options.q['table'][names[i]][j]+'</td>'); //
					//row.push('<td><a href="'+EMEN2WEBROOT+'/record/'+names[i]+'/">'+self.options.q['table'][names[i]][j]+'</a></td>');
					row.push('<td>'+self.options.q['table'][names[i]][j]+'</td>');
				}
				row = '<tr>' + row.join('') + '</tr>';					
				rows.push(row);
			}
			$('tbody', t).empty();
			$('tbody', t).append(rows.join(''));		
		},
		
		event_edit: function(e, param) {
			// Event handler for "Edit" column
			if (this.options.q['count'] > 100) {
				var check = confirm('Editing tables with more than 100 rows may use excessive resources. Continue?');
				if (check==false) {return}
			}
			var self = this;

			//e.stopPropagation();
			// ugly hack..
			var t = $(e.target);
			var key = t.parent().attr('data-name');
			if (key==null) {
				t = $(e.target).parent();
				var key = t.parent().attr('data-name');				
			}
			var selector = '#tbody .editable';
			if (key) {
				selector = '#tbody .editable[data-param='+key+']'
			}			
			t.MultiEditControl({
				show: true,
				selector: selector,
				cb_save: function(caller){self.query()}
			});
		}
	});
})(jQuery);

