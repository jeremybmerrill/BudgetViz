{% macro doJavascript(exp, bill_loop) -%}
                    <script type="text/javascript">
                    {#TODO: Add a document.ready() #}
                    $("div#{{exp.safe_name}}_{{bill_loop.index0}}").qtip({
                           content: '{{exp.display_name}}<br />Total allocation: ${{exp.cost}} <br /> Per student: ${{exp.cost_per}} <br /> {{exp.blurb}}',
                           show: 'mouseover',
                           hide: { when: 'mouseout', fixed: true },
                           position: {
                              target: $("div#text-{{exp.safe_name}}_{{bill_loop.index0}}"),
                              corner: {
                                {% if exp.top != 0: %}
                                 target: 'bottomMiddle',
                                 tooltip: 'topMiddle',
                                {% else: %}
                                 target: 'topMiddle',
                                 tooltip: 'bottomMiddle',
                                {% endif %}            
                              }
                           },
                           style: {
                                {% if exp.top != 0: %}
                                  tip: 'topMiddle'
                                {% else: %}
                                  tip: 'bottomMiddle'
                                {% endif %}
                                {% if 0 in exp.bills or 7 in exp.bills or 13 in exp.bills: %}
                                  , 'max-height': 80, 
                                  width: { min: 0, max: 1000}
                                {% elif 1 in exp.bills or 8 in exp.bills or 14 in exp.bills: %}
                                  , 'max-height': 180,
                                  width: { min: 0, max: 700}
                                {% endif %}
                           }
                       });
                    $("div#text-{{exp.safe_name}}_{{bill_loop.index0}}").qtip({
                           content: '{{exp.display_name}}<br />Total allocation: ${{exp.cost}} <br /> Per student: ${{exp.cost_per}} <br /> {{exp.blurb}}',
                           show: 'mouseover', 
                           hide: { when: 'mouseout', fixed: true },
                           position: {
                              corner: {
                                {% if exp.top != 0: %}
                                 target: 'bottomMiddle',
                                 tooltip: 'topMiddle',
                                {% else: %}
                                 target: 'topMiddle',
                                 tooltip: 'bottomMiddle',
                                {% endif %}            
                              }
                           },
                           style: {
                                {% if exp.top != 0: %}
                                  tip: 'topMiddle'
                                {% else: %}
                                  tip: 'bottomMiddle'
                                {% endif %}
                                {% if 0 in exp.bills or 7 in exp.bills or 13 in exp.bills: %}
                                  , 'max-height': 80, 
                                  width: { min: 0, max: 1000}
                                {% elif 1 in exp.bills or 8 in exp.bills or 14 in exp.bills: %}
                                  , 'max-height': 180,
                                  width: { min: 0, max: 700}
                                {% endif %}
                           }
                    });

                    $('.{{exp.safe_name}}').mouseover(function(){
                        $("div.{{exp.safe_name}}").css("opacity","0.3");
                        $("div.{{exp.safe_name}}").css("backgroundColor","black");
                    });
                    $('.{{exp.safe_name}}').mouseleave(function(){
                        $("div.{{exp.safe_name}}").css("opacity","1.0");
                        $("div.{{exp.safe_name}}").css("backgroundColor","inherit");
                    });
                    </script>
{% endmacro %}

<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01//EN">
<html lang="en">
<head>
    <script type="text/javascript" src="http://ajax.googleapis.com/ajax/libs/jquery/1.6/jquery.min.js"></script>
    <script type="text/javascript" src="jquery.qtip-1.0.0-rc3.min.js"></script>
    <title>laremont Port Sid | ASCMC Budget Viz</title>
    <link rel="stylesheet" type="text/css" href="BudgetViz_public/viz.css" >
    <link href='http://fonts.googleapis.com/css?family=Quattrocento+Sans' rel='stylesheet' type='text/css'>
    <link href='http://fonts.googleapis.com/css?family=Play:400,700' rel='stylesheet' type='text/css'>

</head>
<body>

<div id="thewholething" >
<h1>How Does <span id="ascmc">ASCMC</span> Spend Your Student Fees?</h1>
<p>{{explanatory_paragraph}}</p>
{% set bills_per_side = BILLS_PER_SIDE %}

{% for bill in bills: -%}
    {% set bill_loop = loop %}
    {% if loop.index0 == bills_per_side * 0: -%}
        <div id="left-stuff">
    {% endif -%}
    {% if loop.index0 == bills_per_side * 1: -%}
        <div id="center-stuff">
    {% endif -%}
    {% if loop.index0 == bills_per_side * 2 -%}
        <div id="right-stuff">
    {% endif -%}

    <div class="bill twenty">
    
    {% for tranch in bill -%}
        {% set outer_loop = loop -%}
    <div class="holder" style="float: left;">
        {% for tranch_item in tranch -%}
            <div class="coverer
                {# Determines when to put left/right borders on tranches (so that two tranches representing the same expenditure don't have a border between them.#}
                {% if ((bill[outer_loop.index0-1][0][1].safe_name == tranch_item[1].safe_name) or (bill[outer_loop.index0-1][-1][1].safe_name == tranch_item[1].safe_name)) and (not outer_loop.first): -%}
                    left_continue 
                {% endif -%}
                {% if (not outer_loop.last) and ((bill[outer_loop.index0+1][0][1].safe_name == tranch_item[1].safe_name) or (bill[outer_loop.index0+1][-1][1].safe_name == tranch_item[1].safe_name)): -%}
                    right_continue 
                {% endif -%}
                {% if ((tranch_item[1].top != 0 and False) or (tranch_item[0] < 100)) and outer_loop.index0 != 0 %} {# and this isn't a full tranch #}
                    left_partial
                {% endif -%}
                {% if not outer_loop.last: %}
                    not-rightmost
                {% endif %}
                {% if loop.index0 != 0: %}
                    nontopcoverer
                {% endif %}
                {{tranch_item[1].safe_name}}" id="{{tranch_item[1].safe_name}}_{{bill_loop.index0}}" style="height: {{tranch_item[0]}}%; clear: left;" 
            >
                 <!--This: {{tranch_item[1].safe_name}} Prev: {{bill[loop.index0-1][0][1].safe_name}}  Next: {{bill[loop.index0+1][0][1].safe_name}} {{outer_loop.first}}-->

            </div> {# end .coverer #}
        {% endfor -%} {# end tranch_item in tranch #}
    </div>{# / holder #}
    {% endfor -%} {# end tranch in bill #}

    <div style="clear: both;"></div>

        {% for expenditure in bills_by_exp[loop.index0]: -%}
        <!-- count {{loop.index0}} -->
        <div class="bill-coverer" style="color:white;">
             <div class="text-{{expenditure.safe_name}} name" id="text-{{expenditure.safe_name}}_{{bill_loop.index0}}" style="top: {{2 + expenditure.top}}%; left: {{expenditure.left}}%; width: {{expenditure.text_width}}%;"> 
                <span class="expenditurename">{{expenditure.display_name_split}}</span>
             </div> 
        </div> <!-- /bill-coverer -->
        <script type="text/javascript">
        {% set exp = expenditure -%}
        {#TODO: Add a document.ready() #}
        $("div#{{exp.safe_name}}_{{bill_loop.index0}}").qtip({
               content: '{{exp.display_name}}<br />Total allocation: ${{exp.cost}} <br /> Per student: ${{exp.cost_per}} <br /> {{exp.blurb}}',
               show: {delay: 0, when: 'mouseover'},
               hide: { when: 'mouseout', fixed: true },
               position: {
                  target: $("div#text-{{exp.safe_name}}_{{bill_loop.index0}}"),
                  corner: {
                    {% if exp.top != 2 and exp.top != 0: %}
                     target: 'bottomMiddle',
                     tooltip: 'topMiddle',
                    {% else: %}
                     target: 'topMiddle',
                     tooltip: 'bottomMiddle',
                    {% endif %}            
                  }
               },
               style: {
                    {% if exp.top != 0  and exp.top != 2: %}
                      tip: 'topMiddle'
                    {% else: %}
                      tip: 'bottomMiddle'
                    {% endif %}
                    {% if 0 in exp.bills or 7 in exp.bills or 13 in exp.bills: %}
                      , 'max-height': 80, 
                      width: { min: 0, max: 1000}
                    {% elif 1 in exp.bills or 8 in exp.bills or 14 in exp.bills: %}
                      , 'max-height': 180,
                      width: { min: 0, max: 700}
                    {% endif %}
               }
           });
        $("div#text-{{exp.safe_name}}_{{bill_loop.index0}}").qtip({
               content: '{{exp.display_name}}<br />Total allocation: ${{exp.cost}} <br /> Per student: ${{exp.cost_per}} <br /> {{exp.blurb}}',
               show: 'mouseover', 
               hide: { when: 'mouseout', fixed: true },
               position: {
                  corner: {
                    {% if exp.top != 0  and exp.top != 2: %}
                     target: 'bottomMiddle',
                     tooltip: 'topMiddle',
                    {% else: %}
                     target: 'topMiddle',
                     tooltip: 'bottomMiddle',
                    {% endif %}            
                  }
               },
               style: {
                    {% if exp.top != 0 and exp.top != 2: %}
                      tip: 'topMiddle'
                    {% else: %}
                      tip: 'bottomMiddle'
                    {% endif %}
                    {% if 0 in exp.bills or 7 in exp.bills or 13 in exp.bills: %}
                      , 'max-height': 80, 
                      width: { min: 0, max: 1000}
                    {% elif 1 in exp.bills or 8 in exp.bills or 14 in exp.bills: %}
                      , 'max-height': 180,
                      width: { min: 0, max: 700}
                    {% endif %}
               }
        });

        $('.text-{{exp.safe_name}}').mouseover(function(){
            $("div.{{exp.safe_name}}").css("opacity","0.3");
            $("div.{{exp.safe_name}}").css("backgroundColor","black");
        });
        $('.text-{{exp.safe_name}}').mouseleave(function(){
            $("div.{{exp.safe_name}}").css("opacity","1.0");
            $("div.{{exp.safe_name}}").css("backgroundColor","inherit");
        });
        $('.{{exp.safe_name}}').mouseover(function(){
            $("div.{{exp.safe_name}}").css("opacity","0.3");
            $("div.{{exp.safe_name}}").css("backgroundColor","black");
        });
        $('.{{exp.safe_name}}').mouseleave(function(){
            $("div.{{exp.safe_name}}").css("opacity","1.0");
            $("div.{{exp.safe_name}}").css("backgroundColor","inherit");
        });
        </script>
        {% endfor -%}      



    </div> <!-- /bill -->

{% if loop.index0 == (bills_per_side * 1) - 1 or loop.index0 == (bills_per_side * 2) -1: -%}
      </div> {# The end of the {left-, center-,right-}stuff divs. #}
{% endif -%}

{% if loop.last %}
    {% if loop.index0 < bills_per_side * 2: -%}
        <div id="right-stuff">
    {% endif -%}
    {# Do the coins, smaller bills. #}
    {% for exp in small_bills_and_coins: -%}
        {% for small_bill_amt, small_bill_name in small_bills: -%}
            {% if small_bill_name in exp.bills: -%}
                <!-- smallbilling {{small_bill_name}} for {{exp.safe_name}} -->
                <div class="
                    {% if small_bill_name in ["ten", "five", "one"]: -%}
                        bill
                    {% else: -%}
                        coin {# also need to implement coin-holders #}
                    {% endif -%}
                    {{small_bill_name}}">
                    <div class="whole_bill_holder {{exp.safe_name}}" id="{{exp.safe_name}}_{{bill_loop.index0}}">
                    
                    </div>
                    <div style="clear: both;"></div>
                    <div class="bill-coverer" style="color:white;">
                         <div class="text-{{exp.safe_name}} name" id="text-{{exp.safe_name}}_{{bill_loop.index0}}" style="top: {{2 + exp.top}}%; left: 0%; width: 100%;"> 
                            <span class="expenditurename">{{exp.display_name_split}}</span>
                         </div> 
                    </div> <!-- /bill-coverer -->
                    {{ doJavascript(exp, bill_loop) }}
                </div> <!-- /bill -->
            {% endif %}
        {% endfor %}
        <div class="coin-holder">
        {% for small_bill_amt, small_bill_name in coins: -%}
            {% if small_bill_name in exp.bills: -%}
                <!-- smallbilling {{small_bill_name}} for {{exp.safe_name}} -->
                <div class="
                    {% if small_bill_name in ["ten", "five", "one"]: -%}
                        bill
                    {% else: -%}
                        coin
                    {% endif -%}
                    {{small_bill_name}}">
                    <div class="whole_bill_holder {{exp.safe_name}}" id="{{exp.safe_name}}_{{bill_loop.index0}}">
                    
                    </div>
                    <div style="clear: both;"></div>
                    {% if small_bill_name in ["ten", "five", "one"]: -%}
                    <div class="bill-coverer" style="color: white; width: 100%; height: 100%; top: 2%;">
                         <div class="text-{{exp.safe_name}} name" id="text-{{exp.safe_name}}_{{bill_loop.index0}}" style="top: {{2 + exp.top}}%; left: 0%; width: 100%;"> 
                            <span class="expenditurename">{{exp.display_name_split}}</span>
                         </div> 
                    </div> <!-- /bill-coverer -->
                    {% else %}
                    <div class="bill-coverer" style="color:white; width: 100%; height: 100%; top: 2%;">
                         <div class="text-{{exp.safe_name}} name" id="text-{{exp.safe_name}}_{{bill_loop.index0}}" style="top: 20%; left: 0%; width: {{exp.text_width}}%;"> 
                            <span class="expenditurename">{{exp.display_name_split}}</span>
                         </div> 
                    </div> <!-- /bill-coverer -->
                    {% endif %}
                    {{ doJavascript(exp, bill_loop) }}
                </div> <!-- /bill or coin -->
            {% endif %}
        {% endfor %}
        </div> <!-- end of coin-holder -->
    {% endfor %}
{% endif -%}

{% endfor -%} {# end bill in bills #}
</div> <!-- end of right-stuff -->
<div id="credit">
<a href="http://jeremybmerrill.com/budgetviz.php">BudgetViz</a> by Jeremy B. Merrill
</div> <!--/thewholething -->
<script type="text/javascript">
$(document).ready(function(){
  //$('.expenditurename').hide();
  //$("div.coverer").css("opacity","0.3");
  //$("div.coverer").css("backgroundColor","black");
    $('#text-damages_2').css("font-size", 14);
    $('#text-student_sec_0').css("font-size", 14);
    $('#text-private_sec_5').css("font-size", 14);
    $('#text-private_sec_5').css("top", $('#text-private_sec_5').css("font-size") -2);
    $('.text-wedding').css("font-size", 14);

});
</script>
</body>
</html>

