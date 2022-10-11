#!/usr/bin/env python
# coding: utf-8

# In[1]:


from IPython.core.display import SVG,HTML
import svgwrite


# In[2]:


0.1  -> 1800
0.25 -> 600
0.5  -> 200

0.1  -> 180
0.25 -> 150
0.5  -> 100


# In[10]:


import svgwrite
dwg = svgwrite.Drawing('arrows.svg', (400, 400))
dwg.tostring()


# In[7]:


dwg = svgwrite.Drawing('arrows.svg', (400, 400))

def add_arrow(dwg,name='arrow',scale=1,angle=0,center_x=0,center_y=0,color="#337ab7"):
    trans_x = center_x*(1-scale)
    trans_y = center_y*(1-scale)
    transform = f"translate({trans_x},{trans_y}) scale({scale})  rotate({angle},{center_x},{center_y})"
    line = dwg.add(dwg.path(d="M 200,200 h 1.32292 v -52.916665 h 1.32291 l -2.64583,-5.291666 -2.64583,5.291666 h 1.32291 v 52.916665 z",
                        id=name,
                        transform=transform,fill=color, stroke="black", stroke_width="0",
                        onmouseover="showMyTooltip(evt)"))
    
    return line


add_arrow(dwg,name='arrow_1',scale=0.5,angle=10,center_x=200,center_y=200)
add_arrow(dwg,name='arrow_2',scale=2,  angle=20,center_x=200,center_y=200)
add_arrow(dwg,name='arrow_3',scale=1,  angle=90,center_x=200,center_y=200)
line = add_arrow(dwg,name='arrow_4',scale=0.1,angle=180,center_x=200,center_y=200)
dwg.save()

#line.set_metadata("<data 'hola'/>")
#from xml.etree.ElementTree import ElementTree
import xml.etree.ElementTree as ET

element = ET.Element('data',{"value":"2"})
line.set_metadata(element)
print(line.tostring())

html_string = '''
<!DOCTYPE html>
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
  <title>Mode Shapes</title>

</head>
<body style='font-family:arial'>
<center>
<b>Mode Shapes</b><br /><br />
Below are 3 elements with an onmouseover event and their data attribute.<br />
<br />
<div style='width:90%;background-color:gainsboro;text-align:justify;padding:10px;border-radius:6px;'>
A DIV, that is placed over the inline SVG, is the most diversified means of showing data related to an SVG element. The element can be highlighted and the DIV can
include the associated data attached to the element. The DIV is positioned at the element taking into consideration the web page scrolled position.
</div>
<p></p>
<div id="svgDiv" style='background-color:gainsboro;width:400px;height:400px;'>
{svg_string}
</div>
<div id=tooltipDiv style='background:white;padding:5px;position:absolute;top:0px;left:0px;visibility:hidden'></div>

</body>
<script>

var PreviousElement
//---mouseover element--
function showMyTooltip(evt)
{
    var target = evt.target
   if(!PreviousElement||PreviousElement!=target) //--prevent 'stutter'---
   {
        if(PreviousElement) //---remove highlight (stroke) ---
            PreviousElement.setAttribute('stroke-width',0)

        target.setAttribute('stroke-width',3)

        var myData=target.getAttribute("id")
        tooltipDiv.innerHTML=myData

        var x = evt.clientX;
        var y = evt.clientY;

        var scrollX = window.pageXOffset
        var scrollY = window.pageYOffset

        var divLeft=x+0+scrollX +"px"//-- ---
        var divTop= y+0+scrollY +"px"//-- +scrollY+"px"---

        tooltipDiv.style.left=divLeft
        tooltipDiv.style.top=divTop
        tooltipDiv.style.visibility="visible"
        PreviousElement=target
  }
}

</script>

</html>
'''

svg_string = '''<svg baseProfile="full" height="400" version="1.1" width="400" xmlns="http://www.w3.org/2000/svg" xmlns:ev="http://www.w3.org/2001/xml-events" xmlns:xlink="http://www.w3.org/1999/xlink"><defs /><path d="M 200,200 h 1.32292 v -52.916665 h 1.32291 l -2.64583,-5.291666 -2.64583,5.291666 h 1.32291 v 52.916665 z" fill="#337ab7" id="omega_1" onmouseover="showMyTooltip(evt)" stroke="black" stroke-width="0" transform="translate(190.66837501299696,190.66837501299696) scale(0.04665812493501516)  rotate(-47.12184765165722,200,200)" /><path d="M 200,200 h 1.32292 v -52.916665 h 1.32291 l -2.64583,-5.291666 -2.64583,5.291666 h 1.32291 v 52.916665 z" fill="#337ab7" id="omega_2" onmouseover="showMyTooltip(evt)" stroke="black" stroke-width="0" transform="translate(185.31037320772722,185.31037320772722) scale(0.07344813396136383)  rotate(121.61175094189778,200,200)" /><path d="M 200,200 h 1.32292 v -52.916665 h 1.32291 l -2.64583,-5.291666 -2.64583,5.291666 h 1.32291 v 52.916665 z" fill="#337ab7" id="omega_3" onmouseover="showMyTooltip(evt)" stroke="black" stroke-width="0" transform="translate(5.561535723657229,5.561535723657229) scale(0.9721923213817139)  rotate(76.24500156225037,200,200)" /><path d="M 200,200 h 1.32292 v -52.916665 h 1.32291 l -2.64583,-5.291666 -2.64583,5.291666 h 1.32291 v 52.916665 z" fill="#337ab7" id="omega_4" onmouseover="showMyTooltip(evt)" stroke="black" stroke-width="0" transform="translate(-200.0,-200.0) scale(2.0)  rotate(-101.51030400833254,200,200)" /></svg>'''


html_string = html_string.replace('{svg_string}',svg_string)
HTML(html_string)


# In[266]:


from xml.etree.ElementTree import ElementTree
tree = ElementTree()
tree.


# In[8]:


html_string = '''
<!DOCTYPE html>
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
  <title>Mode Shapes</title>

</head>
<body style='font-family:arial'>
<center>
<b>Mode Shapes</b><br /><br />
Below are 3 elements with an onmouseover event and their data attribute.<br />
<br />
<div style='width:90%;background-color:gainsboro;text-align:justify;padding:10px;border-radius:6px;'>
A DIV, that is placed over the inline SVG, is the most diversified means of showing data related to an SVG element. The element can be highlighted and the DIV can
include the associated data attached to the element. The DIV is positioned at the element taking into consideration the web page scrolled position.
</div>
<p></p>
<div id="svgDiv" style='background-color:gainsboro;width:400px;height:400px;'>
{svg_string}
</div>
<div id=tooltipDiv style='background:white;padding:5px;position:absolute;top:0px;left:0px;visibility:hidden'></div>

</body>
<script>

var PreviousElement
//---mouseover element--
function showMyTooltip(evt)
{
    var target = evt.target
   if(!PreviousElement||PreviousElement!=target) //--prevent 'stutter'---
   {
        if(PreviousElement) //---remove highlight (stroke) ---
            PreviousElement.setAttribute('stroke-width',0)

        target.setAttribute('stroke-width',3)

        var myData=target.getAttribute("id")
        tooltipDiv.innerHTML=myData

        var x = evt.clientX;
        var y = evt.clientY;

        var scrollX = window.pageXOffset
        var scrollY = window.pageYOffset

        var divLeft=x+0+scrollX +"px"//-- ---
        var divTop= y+0+scrollY +"px"//-- +scrollY+"px"---

        tooltipDiv.style.left=divLeft
        tooltipDiv.style.top=divTop
        tooltipDiv.style.visibility="visible"
        PreviousElement=target
  }
}

</script>

</html>
'''

svg_string = '''<svg baseProfile="full" height="400" version="1.1" width="400" xmlns="http://www.w3.org/2000/svg" xmlns:ev="http://www.w3.org/2001/xml-events" xmlns:xlink="http://www.w3.org/1999/xlink"><defs /><path d="M 200,200 h 1.32292 v -52.916665 h 1.32291 l -2.64583,-5.291666 -2.64583,5.291666 h 1.32291 v 52.916665 z" fill="#337ab7" id="omega_1" onmouseover="showMyTooltip(evt)" stroke="black" stroke-width="0" transform="translate(190.66837501299696,190.66837501299696) scale(0.04665812493501516)  rotate(-47.12184765165722,200,200)" /><path d="M 200,200 h 1.32292 v -52.916665 h 1.32291 l -2.64583,-5.291666 -2.64583,5.291666 h 1.32291 v 52.916665 z" fill="#337ab7" id="omega_2" onmouseover="showMyTooltip(evt)" stroke="black" stroke-width="0" transform="translate(185.31037320772722,185.31037320772722) scale(0.07344813396136383)  rotate(121.61175094189778,200,200)" /><path d="M 200,200 h 1.32292 v -52.916665 h 1.32291 l -2.64583,-5.291666 -2.64583,5.291666 h 1.32291 v 52.916665 z" fill="#337ab7" id="omega_3" onmouseover="showMyTooltip(evt)" stroke="black" stroke-width="0" transform="translate(5.561535723657229,5.561535723657229) scale(0.9721923213817139)  rotate(76.24500156225037,200,200)" /><path d="M 200,200 h 1.32292 v -52.916665 h 1.32291 l -2.64583,-5.291666 -2.64583,5.291666 h 1.32291 v 52.916665 z" fill="#337ab7" id="omega_4" onmouseover="showMyTooltip(evt)" stroke="black" stroke-width="0" transform="translate(-200.0,-200.0) scale(2.0)  rotate(-101.51030400833254,200,200)" /></svg>'''


html_string = html_string.replace('{svg_string}',svg_string)
HTML(html_string)


# In[3]:


HTML('''
?php
  declare(strict_types=1);

  // function fred($val) {echo '<pre>'.print_r($val,1). '</pre>';}
  $title = 'SVG Chart MouserOver ToolTips-001';
  $sp    = 'https://www.sitepoint.com/community/t/do-you-know-a-simple-solution-to-this-svg-javascript-problem/235078';

  // CREATE Columns
  $lines = '';
  for($x=100; $x<1600; $x+=60):
    $px   = mt_rand(100,800);
    $yPos = 900 -  $px;
    $temp = sprintf('%2.1f ', 20 + $px/500);

    $iDate = time() + 60*60*$x;
    $dDate = "'".date('D d M Y H:i', $iDate) ."'";

    $lines .= <<< ______TMP
      <line
        onmouseover="mouseover($dDate, $temp, $x, $yPos)" 
        onmouseout="mouseout()" 
        x1="$x" 
        y1="900" 
        x2="$x" 
        y2="$yPos" 
        stroke-width="42"/>
______TMP;

  endfor;  

// CREATE x-Axis
 $xaxis = '';
 $y = 17;
 for($x=100; $x<=1620; $x+=200):
  $yy = sprintf('%0.2f',$y);
  
  $xaxis .= "\n" 
         .'<text x="'.$x.'" y="915" font-size="14">| </text>'
         .'<text x="'.$x.'" y="930" font-size="24">'.$yy.'</text>';
  $y += 0.10;
 endfor;

// CREATE Blurb
$blurb = <<< ____TMP
  <text x="40" y="80" stroke="red" font-size="17" text-anchor="start">23.0</text>
  <path d="M 15 80 L 1600 80 "   style="stroke:#ccc; stroke-width: 2.5;"></path>
  <text x="40" y="500" stroke="red" font-size="17" text-anchor="start">22.0</text>
  <path d="M 15 500 L 1600 500 " style="stroke:#ccc; stroke-width: 2.5;"></path>
  <text x="40" y="920" stroke="red" font-size="17" text-anchor="start">21.0</text>
  <path d="M 15 920 L 1600 920 " style="stroke:#ccc; stroke-width: 2.5;"></path>
  <path d="M 65 40 L 65 940 "    style="stroke:#ccc; stroke-width:1.9;"></path>
  <text x="18"  y="500"  transform="rotate(270,18,500 )">Temperature</text>
  <path d="M 85 0 L 85 950 " style="stroke:#999; stroke-width: 1.5;"></path>

  <text x="81%" y="40"  font-size="32">Problem with ToolTips</text>
  <text x="81%" y="100" font-size="28" text-anchor="start">Snapshot:</text>
  <text x="82%" y="140" font-size="28" text-anchor="start">Mon, Aug 29th 05:47</text>
  <text x="81%" y="200" font-size="28" text-anchor="start">striving to keep you cool</text>
____TMP;


?><!DOCTYPE HTML>
<html lang="en-gb">
<head>
<title> <?= $title ?> </title>  
<meta http-equiv="content-type" content="text/html; charset=utf-8"/>
<meta name="viewport" content="width=device-width, initial-scale=1"/>
<meta name="robots"   content="index, nofollow" />
<link rel=icon href="/faviclon.ico" type="image/ico"/>
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<!-- <link href="../style.css" media="all" rel="stylesheet"> -->
<style type="text/css">
  .bdr {border:solid 1px #ccc;}
  .flr {float:right;}
  .ngs {background-color: snow;}
  .ooo {border:0; margin:0; padding:0;}
  .mga {margin:auto;}
  .tac {text-align: center;}
  .w88 {width:88%; max-width:960px;}

  svg line {
    stroke:blue;
    stroke-dasharray:  1000;
    stroke-dashoffset: 1000;
    animation: dashline 2s linear alternate forwards;
    animation-name: dashline; 
  }
  svg line:hover {opacity: 0.5; stroke:snow !important;}
  @keyframes dashline {
    from {stroke-dashoffset: 1000;}
    to   {stroke-dashoffset: 0;}
  }
  @keyframes dashline {to   {stroke-dashoffset: 0;} }    /* FireFox */
  #svgT {
    -webkit-user-callout: none;/* PaulOBriend's table hover  disable magnifying glass */
    -webkit-user-select: none; /* disable magnifying glass */
  }
</style>

</head>
<body>
<h4 class="ooo flr"> <a href="<?= $sp ?>" > SitePoint Forum </a> </h4>
<h5 class="ooo"> &nbsp; <a href="./"> Menu</a> &nbsp;&nbsp; <a href="?x=123">Refresh</a> </h5>
<hr />
<h1 class="tac"> <?= $title ?> </h1>

<div class="w88 mga bdr bgs">
  <svg id="svgT" viewBox="0 0 2000 1000" xml:space="preserve">
    <rect x="000" y="00" width="80%" height="100%" fill="#ccc"></rect>
    <text x="20%" y="50" font-size="48">Using MouseOver() for ToolTips</text>

    <?= $blurb ?>
    <?= $xaxis ?>
    <?= $lines ?> 

    <g font-size="25">
      <rect 
        id="tRct" 
        width="14em" height="2.42em" 
        fill="transparent"
      />
      <!-- rx="-999" ry="999" -->

      <text id="tTip"></text><!-- Date to go here -->
      <text id="tBox"></text><!-- Temperature to go here -->
    </g>
  </svg>

</div>
<div> <br><br> </div>

<script type="text/javascript">
function mouseover(date, temp, xPos, yPos) {
  document.getElementById("tRct").style.fill = "snow";
  document.getElementById("tRct").x.baseVal.value = xPos- 10;
  document.getElementById("tRct").y.baseVal.value = yPos- 64;

  document.getElementById("tTip").innerHTML  = date;
//document.getElementById("tTip").style.fill = "red";
  document.getElementById("tTip").setAttribute('x',xPos);
  document.getElementById("tTip").setAttribute('y',yPos-40);

  document.getElementById("tBox").innerHTML  = temp +"&#178;C";
//document.getElementById("tBox").style.fill = "darkgreen";
  document.getElementById("tBox").setAttribute('x',xPos+75);
  document.getElementById("tBox").setAttribute('y',yPos-09);
}

function mouseout() {
  document.getElementById("tRct").x.baseVal.value = -99999;
  document.getElementById("tTip").innerHTML = "";
  document.getElementById("tBox").innerHTML = "";
}
</script>

<h3 class="ooo">Source: </h3>
<div class="w88 mga bgs bdr">
  <?php highlight_file(__FILE__) ?>
</div>

</body>
</html>
''')


# In[ ]:




