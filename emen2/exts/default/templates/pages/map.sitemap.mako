<%! import jsonrpc.jsonutil  %>
<%inherit file="/page" />
<%namespace name="relmap" file="/pages/map"  /> 

<%block name="js_ready">
	$("#sitemap").BrowseControl({
		root: ${jsonrpc.jsonutil.encode(root)},
		controls: $('#sitemap'),
		show: true,
		embed: true,
	});
</%block>

<h1>Site Map</h1>

## ${relmap.traverse(tree, root, recnames, recurse, mode=mode, keytype=keytype, expandable=expandable, id='sitemap')}

<div id="sitemap"></div>