<%! 
import jsonrpc.jsonutil 
import random
%>
<%inherit file="/page" />

<%block name="js_ready">
    ${parent.js_ready()}
    // Intialize the Tab controller
    var tab = $("#e2-tab-query");        
    tab.TabControl({});
</%block>

<div class="e2-tab e2-tab-switcher">
    <ul class="e2l-cf">
        <li class="e2-tab-active" data-tab="keywords">Keywords</li>
    </ul>
    
    <div class="e2-tab-active" data-tab="keywords">
        This is a development version of the database. The query form is currently being redesigned, and will be back soon.
    </div>
</div>
