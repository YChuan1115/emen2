// js is stupid at sorting.
function sortNumber(a, b) {
	return a - b;
}


/// switch.js
function switchbutton(type,id) {
	$(".button_"+type).each(function() {
		var elem=$(this);
		if (this.id != "button_"+type+"_"+id) {
			elem.removeClass("button_active");
			elem.removeClass("button_"+type+"_active");
		} else {
			elem.addClass("button_active");
			elem.addClass("button_"+type+"_active");
		}
	});
}


var switchedin=new Array();

function switchin(classname, id) {
	switchedin[classname]=id;
	switchbutton(classname,id);
	$(".page_"+classname).removeClass("page_active");
	$(".page_"+classname).removeClass("page_"+classname+"_active");	
	$("#page_"+classname+"_"+id).addClass("page_active");
	$("#page_"+classname+"_"+id).addClass("page_"+classname+"_active");
}



//////////////////////////////////////////
// access values from cached sources

var caches = {};
caches["paramdefs"] = {};
caches["recorddefs"] = {};
caches["displaynames"] = {};
caches["groupnames"] = {};
caches["users"] = {};
caches["groups"] = {};
caches["recs"] = {};
caches["recnames"] = {};
caches["children"] = {};
caches["parents"] = {};
caches["colors"] = {};

//////////////////////////////////////////


function notify(msg, fade, error) {
	var msg=$('<li>'+msg+'</li>');

	if (error) {
		msg.addClass("error");
	}

	//var killbutton = $('<img src="'+EMEN2WEBROOT+'/images/delete.png" />');
	var killbutton = $('<span>X</span>');
	killbutton.click(function() {
		$(this).parent().fadeOut(function(){
			//fadeoutcallback; in this context, 'this' is li
			$(this).remove();
			});		
	});
	killbutton.addClass("kill");
	msg.append(killbutton);

	// auto fade if given time value
	//if (!fade) {
	//	setTimeout(function(){msg.fadeOut()},3000)
	//}
	//if (fade > 0) {
	//	setTimeout(function(){msg.fadeOut()},fade*1000)
	//}

	$("#alert").append(msg); //.fadeIn();
	
}


function notify_post(uri,msgs) {
  var postform = document.createElement("form");
  postform.method="POST" ;
  postform.action = uri;
	for (var i=0;i<msgs.length;i++) {
		var note = document.createElement("input") ;
		note.setAttribute("name", "notify___"+i) ;
		note.setAttribute("value", msgs[i]);
		postform.appendChild(note) ;
	}
	document.body.appendChild(postform);
  postform.submit();	
}




function newrecord_init(rec) {
	rec.recid = "None";
	var recid = rec.recid;
	caches["recs"][recid] = rec;

	$(".editbar .tools").EditbarHelper({
		width:400,
		height:300,
		show: true,
		cb: function(self) {
			var r = $("#rendered");
			if (!r.hasClass('editbar-reflow')) {
				r.addClass('editbar-reflow');
				r.css('padding-top', self.popup.height()+10);
			} else {
				r.removeClass('editbar-reflow');
				r.css('padding-top', 0);			

			}
		}
	});	

	$('#newrecord_save').MultiEditControl({
		recid: recid,
		show: true
		});
	
	$('#newrecord_permissions').PermissionControl({
		recid:recid,
		edit:true,
		embed:true
		});

	$('.editable').EditControl({
		recid: recid
		});

	// Change the text of file upload elements..
	$('.editable_files .label').html('(The record must be saved before files can be attached)');

	$('.editbar .change select').change(function(){
		var parent = $(this).attr('data-parent');
		notify_post(EMEN2WEBROOT+'/db/record/'+parent+'/new/'+$(this).val()+'/', []);
	});


}

function record_init(rec, ptest, edit) {
	var recid = rec.recid;
	caches["recs"][recid] = rec;

	$('.editbar .edit').MultiEditControl({});
	$('.editable').EditControl({});
	$('.editable_files').FileControl({});

	$('.editbar .permissions').EditbarHelper({
		width: 620,
		height: 400,
		cb: function(self){
			self.popup.PermissionControl({
				recid: recid,
				edit: ptest[3],
				embed: true,
				show: true
				});
			}
	});		


	$('.editbar .attachments').EditbarHelper({
		width: 620,
		height: 400,
		cb: function(self) {
			self.popup.AttachmentViewerControl({
				recid: recid,
				edit: ptest[2] || ptest[3],
				embed: true,
				show: true
				});
			}
	});		


	$('.editbar .newrecord').EditbarHelper({
		width: 300,
		height: 400,
		cb: function(self){
			self.popup.NewRecordSelect({
				recid: recid,
				embed: true,
				show: true
				});
			}
	});		


	$(".editbar .relationships").EditbarHelper({		
		width: 800,
		height: 400,
		cb: function(self){
			self.popup.RelationshipControl({
				recid: recid,
				edit: true,
				embed: true,
				show: true
				});
			}
	});	
	
	$(".editbar .tools").EditbarHelper({});	

	$(".editbar .selectview").EditbarHelper({});	

	$("#page_comments_comments").CommentsControl({
		recid:recid,
		edit:ptest[1] || ptest[2] || ptest[3],
		title:"#button_comments_comments"
		});
		
	$("#page_comments_history").HistoryControl({
		recid:recid,
		title:"#button_comments_history"
		});

	$('.selectview select').change(function(){
		var target=$("#rendered");
		target.attr("data-viewtype", $(this).val());
		rebuildviews("#rendered");
	});

	if (edit) {
		$('.editbar .edit').MultiEditControl('event_click');
	}

	
}



function record_update(rec) {
	if (typeof(rec)=="number") {
		var recid = rec;
	} else {
		caches["recs"][rec.recid] = rec;
		var recid = rec.recid;
	}
	rebuildviews('.view[data-recid='+recid+']');
	$("#page_comments_comments").CommentsControl('rebuild');
	$("#page_comments_history").HistoryControl('rebuild');
	$('.editbar .attachments').AttachmentViewerControl('rebuild');	
}



function rebuildviews(selector) {
	selector = selector || '.view';
	var self = this;
	$(selector).each(function() {
		var elem = $(this);
		var recid = parseInt(elem.attr('data-recid'));
		var viewtype = elem.attr('data-viewtype');
		var mode = elem.attr('data-mode') || 'html';
		$.jsonRPC("renderview", {'recs':recid, 'viewtype': viewtype, 'mode':mode}, function(view) {
			elem.html(view);
			$('.editable', elem).EditControl({});
			$('.editable_files', elem).FileControl({});
		},
		function(view){}
		);
	})
}


(function($) {
    $.widget("ui.EditbarHelper", {
		options: {
			open: function(self) {},
			close: function(self) {},
			cb: function(self) {},
			init: function(self) {},
			bind: true,
			width: 200,
			height: 200,
			show: false
		},
				
		_create: function() {
			this.built = 0;
			var self = this;
			this.element.addClass('popup');
			if (this.options.bind) {
				this.element.click(function(e) {
					e.stopPropagation();
					self.toggle();
				});
			}
			if (this.options.show) {
				this.toggle();
			}
		},
		
		toggle: function() {
			if (this.element.hasClass('active')) {
				this.hide();
			} else {
				this.show();
			}
		},
		
		show: function() {
			$('.editbar .active').EditbarHelper('hide');
			this.build();
			this.element.addClass('active');
			this.options.cb(this);
			this.options.open(this);
			this.popup.show();
		},
		
		hide: function() {
			if (!this.built) {return}
			this.popup.hide();
			this.options.cb(this);
			this.options.close(this);
			this.element.removeClass('active');
		},		
		
		build: function() {
			if (this.built) {
				return
			}
			this.built = 1;			
			
			var pos = this.element.position();

			this.popup = $('.hidden', this.element);
			if (!this.popup.length) {
				this.popup = $('<div class="hidden" />');
				this.element.after(this.popup);
			}

			this.popup.width(this.options.width);
			this.popup.height(this.options.height);
			this.popup.css('left', this.element.position().left-1);
			this.popup.css('top', this.element.outerHeight()+this.element.position().top-1);
			
			// ugly horrible hack time...
			var uglydiv = $('<div style="position:absolute;background:white" />');
			uglydiv.width(this.element.outerWidth()-3);
			uglydiv.height(4);
			uglydiv.css('left', 0);
			uglydiv.css('top', -4);
			this.popup.append(uglydiv);
			
			this.options.init(this);

		
		},
				
		destroy: function() {
		},
		
		_setOption: function(option, value) {
			$.Widget.prototype._setOption.apply( this, arguments );
		}
	});
})(jQuery);





function escapeHTML(html) {
	var escaped = html;
	var findReplace = [[/&/g, "&amp;"], [/</g, "&lt;"], [/>/g, "&gt;"], [/"/g, "&quot;"]];
	for (var i=0; i < findReplace.length; i++) {
		item = findReplace[i];
    	escaped = escaped.replace(item[0], item[1]);
	}
	return escaped
}
