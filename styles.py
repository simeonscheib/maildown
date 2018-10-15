github = "body,table tr{background-color:#fff}table tr td,table tr th{border:1px solid #ccc;text-align:left;padding:6px 13px;margin:0}pre code,table,table tr{padding:0}hr,pre code{background:0 0}body{font:16px Helvetica,Arial,sans-serif;line-height:1.4;color:#333;word-wrap:break-word;padding:10px 15px}strong,table tr th{font-weight:700}h1{font-size:2em;margin:.67em 0;text-align:center}h2{font-size:1.75em}h3{font-size:1.5em}h4{font-size:1.25em}h1,h2,h3,h4,h5,h6{font-weight:700;position:relative;margin-top:15px;margin-bottom:15px;line-height:1.1}h1,h2{border-bottom:1px solid #eee}hr{height:0;margin:15px 0;overflow:hidden;border:0;border-bottom:1px solid #ddd}a{color:#4183C4}a.absent{color:#c00}ol,ul{padding-left:15px;margin-left:5px}ol{list-style-type:lower-roman}table tr{border-top:1px solid #ccc;margin:0}table tr:nth-child(2n){background-color:#aaa}table tr td :first-child,table tr th :first-child{margin-top:0}table tr td:last-child,table tr th :last-child{margin-bottom:0}img{max-width:100%}blockquote{padding:0 15px;border-left:4px solid #ccc}code,tt{margin:0 2px;padding:0 5px;white-space:nowrap;border:1px solid #eaeaea;background-color:#f8f8f8;border-radius:3px}pre code{margin:0;white-space:pre;border:none}.highlight pre,pre{background-color:#f8f8f8;border:1px solid #ccc;font-size:13px;line-height:19px;overflow:auto;padding:6px 10px;border-radius:3px}"
codehilite_css = '''
.codehilitetable {border 1px;}
.codehilite .hll { background-color: #ffffcc }
.codehilite  { background: #f8f8f8; }
.codehilite .c { color: #408080; font-style: italic } /* Comment */
.codehilite .err { border: 1px solid #FF0000 } /* Error */
.codehilite .k { color: #008000; font-weight: bold } /* Keyword */
.codehilite .o { color: #666666 } /* Operator */
.codehilite .ch { color: #408080; font-style: italic } /* Comment.Hashbang */
.codehilite .cm { color: #408080; font-style: italic } /* Comment.Multiline */
.codehilite .cp { color: #BC7A00 } /* Comment.Preproc */
.codehilite .cpf { color: #408080; font-style: italic } /* Comment.PreprocFile */
.codehilite .c1 { color: #408080; font-style: italic } /* Comment.Single */
.codehilite .cs { color: #408080; font-style: italic } /* Comment.Special */
.codehilite .gd { color: #A00000 } /* Generic.Deleted */
.codehilite .ge { font-style: italic } /* Generic.Emph */
.codehilite .gr { color: #FF0000 } /* Generic.Error */
.codehilite .gh { color: #000080; font-weight: bold } /* Generic.Heading */
.codehilite .gi { color: #00A000 } /* Generic.Inserted */
.codehilite .go { color: #888888 } /* Generic.Output */
.codehilite .gp { color: #000080; font-weight: bold } /* Generic.Prompt */
.codehilite .gs { font-weight: bold } /* Generic.Strong */
.codehilite .gu { color: #800080; font-weight: bold } /* Generic.Subheading */
.codehilite .gt { color: #0044DD } /* Generic.Traceback */
.codehilite .kc { color: #008000; font-weight: bold } /* Keyword.Constant */
.codehilite .kd { color: #008000; font-weight: bold } /* Keyword.Declaration */
.codehilite .kn { color: #008000; font-weight: bold } /* Keyword.Namespace */
.codehilite .kp { color: #008000 } /* Keyword.Pseudo */
.codehilite .kr { color: #008000; font-weight: bold } /* Keyword.Reserved */
.codehilite .kt { color: #B00040 } /* Keyword.Type */
.codehilite .m { color: #666666 } /* Literal.Number */
.codehilite .s { color: #BA2121 } /* Literal.String */
.codehilite .na { color: #7D9029 } /* Name.Attribute */
.codehilite .nb { color: #008000 } /* Name.Builtin */
.codehilite .nc { color: #0000FF; font-weight: bold } /* Name.Class */
.codehilite .no { color: #880000 } /* Name.Constant */
.codehilite .nd { color: #AA22FF } /* Name.Decorator */
.codehilite .ni { color: #999999; font-weight: bold } /* Name.Entity */
.codehilite .ne { color: #D2413A; font-weight: bold } /* Name.Exception */
.codehilite .nf { color: #0000FF } /* Name.Function */
.codehilite .nl { color: #A0A000 } /* Name.Label */
.codehilite .nn { color: #0000FF; font-weight: bold } /* Name.Namespace */
.codehilite .nt { color: #008000; font-weight: bold } /* Name.Tag */
.codehilite .nv { color: #19177C } /* Name.Variable */
.codehilite .ow { color: #AA22FF; font-weight: bold } /* Operator.Word */
.codehilite .w { color: #bbbbbb } /* Text.Whitespace */
.codehilite .mb { color: #666666 } /* Literal.Number.Bin */
.codehilite .mf { color: #666666 } /* Literal.Number.Float */
.codehilite .mh { color: #666666 } /* Literal.Number.Hex */
.codehilite .mi { color: #666666 } /* Literal.Number.Integer */
.codehilite .mo { color: #666666 } /* Literal.Number.Oct */
.codehilite .sa { color: #BA2121 } /* Literal.String.Affix */
.codehilite .sb { color: #BA2121 } /* Literal.String.Backtick */
.codehilite .sc { color: #BA2121 } /* Literal.String.Char */
.codehilite .dl { color: #BA2121 } /* Literal.String.Delimiter */
.codehilite .sd { color: #BA2121; font-style: italic } /* Literal.String.Doc */
.codehilite .s2 { color: #BA2121 } /* Literal.String.Double */
.codehilite .se { color: #BB6622; font-weight: bold } /* Literal.String.Escape */
.codehilite .sh { color: #BA2121 } /* Literal.String.Heredoc */
.codehilite .si { color: #BB6688; font-weight: bold } /* Literal.String.Interpol */
.codehilite .sx { color: #008000 } /* Literal.String.Other */
.codehilite .sr { color: #BB6688 } /* Literal.String.Regex */
.codehilite .s1 { color: #BA2121 } /* Literal.String.Single */
.codehilite .ss { color: #19177C } /* Literal.String.Symbol */
.codehilite .bp { color: #008000 } /* Name.Builtin.Pseudo */
.codehilite .fm { color: #0000FF } /* Name.Function.Magic */
.codehilite .vc { color: #19177C } /* Name.Variable.Class */
.codehilite .vg { color: #19177C } /* Name.Variable.Global */
.codehilite .vi { color: #19177C } /* Name.Variable.Instance */
.codehilite .vm { color: #19177C } /* Name.Variable.Magic */
.codehilite .il { color: #666666 } /* Literal.Number.Integer.Long */
'''

admonition = '''
.attention {background-color: #f0f7fb;
     border: solid 1px #3498db;
     border-radius: 6px;
     line-height: 18px;
     overflow: hidden;
     padding: 11px;} 
.caution {background-color: #ffdddd;
     border: solid 1px #f44336;
     border-radius: 6px;
     line-height: 18px;
     overflow: hidden;
     padding: 11px;}
.danger {background-color: #ffdddd;
     border: solid 1px #f44336;
     border-radius: 6px;
     line-height: 18px;
     overflow: hidden;
     padding: 11px;}
.error {background-color: #ffdddd;
     border: solid 1px #f44336;
     border-radius: 6px;
     line-height: 18px;
     overflow: hidden;
     padding: 11px;}
.hint {background-color: #ddffdd;
     border: solid 1px #4CAF50;
     border-radius: 6px;
     line-height: 18px;
     overflow: hidden;
     padding: 11px;}
.important {background-color: #f0f7fb;
     border: solid 1px #3498db;
     border-radius: 6px;
     line-height: 18px;
     overflow: hidden;
     padding: 11px;}
.note {background-color: #f0f7fb;
     border: solid 1px #3498db;
     border-radius: 6px;
     line-height: 18px;
     overflow: hidden;
     padding: 11px;}
.tip {background-color: #ddffdd;
     border: solid 1px #4CAF50;
     border-radius: 6px;
     line-height: 18px;
     overflow: hidden;
     padding: 11px;}
.warning {background-color: #ffffcc;
     border: solid 1px #ffeb3b;
     border-radius: 6px;
     line-height: 18px;
     overflow: hidden;
     padding: 11px;}
'''
