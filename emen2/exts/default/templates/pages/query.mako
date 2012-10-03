<%! 
import jsonrpc.jsonutil
import uuid
%>

<%def name="table(q, parent=None, rectype=None, qc=True, header=True, controls=True)">
    <%
        tname = uuid.uuid4().hex
    %>
    <script type="text/javascript">
    //<![CDATA[
        var q${tname} = ${jsonrpc.jsonutil.encode(q)};
        $(document).ready(function() {
            $("#${tname}").TableControl({
                q: q${tname}, 
                rectype: ${jsonrpc.jsonutil.encode(rectype)},
                parent: ${jsonrpc.jsonutil.encode(parent)},
                header: ${jsonrpc.jsonutil.encode(header)},
                controls: ${jsonrpc.jsonutil.encode(controls)},
                qc: ${jsonrpc.jsonutil.encode(qc)}
            })
        });    
    //]]>
    </script>

    <div class="e2-query" id="${tname}">
        
        % if controls:
            <div class="e2-tab e2-tab-editbar" data-tabgroup="query" role="tab">
                <ul class="e2-query-header e2l-cf" role="tablist"></ul>
            </div>

            <div class="e2-tab e2-tab-editbar" data-tabgroup="query" role="tabpanel"></div>
        % endif

        ## This form is used for editing table cells
        <form class="e2-query-tableform" method="post" action="${ctxt.reverse('Records/edit')}">
            ## <input type="hidden" name="_redirect" value="" />
            <table class="e2-query-table e2l-shaded" cellspacing="0" cellpadding="0"> 

                % if header:
                    <thead>
                        % for v in q['table']['headers'].get(None, []):
                            <th><div data-name="${v[2]}" data-args="${v[3]}">${v[0]}</div></th>
                        % endfor
                    </thead>
                % endif

                <tbody>
            
                    % if not q['names']:
                        <tr><td colspan="0">No Records found for this query.</td></tr>
                    % endif

                    % for rowid, name in enumerate(q['names']):
                        <tr>
                    
                        ## <td>
                        ##     <input type="checkbox" data-name="${name}" />
                        ## </td>
                                        
                        % for v in q['table'].get(name, []):
                            <td>${v}</td>
                        % endfor
                        </tr>
                    % endfor            
                </tbody>

            </table>
        
        </form>
        
    </div>
    
</%def>

${table(q, rectype=rectype, parent=parent, header=header, controls=controls, qc=False)}
