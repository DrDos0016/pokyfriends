if (!($ = window.jQuery)) { // typeof jQuery=='undefined' works too
script = document.createElement( 'script' );
script.src = 'https://ajax.googleapis.com/ajax/libs/jquery/3.4.1/jquery.min.js';
script.onload=Setup;
document.body.appendChild(script);
}
else {
Setup();
}

//Default color
var color = "black";

function highlight()
{
var selection= window.getSelection().getRangeAt(0);
var selectedText = selection.extractContents();
var span= document.createElement("span");

span.style.backgroundColor = color;
span.style.color = color;
span.appendChild(selectedText);
selection.insertNode(span);
}

function Setup()
{
$('head').append('<style>.blackout{background-color:#000;color:#333;}.whiteout{background-color:#fff;color:#CCC;}.redout{background-color:#f00;color:#C00;}.greenout{background-color:#0f0;color:#0C0;}.blueout{background-color:#00f;color:#00C;}.pinkout{background-color:#FF1493;color:#CC0060;}.color{border:1px dotted #CCCCCC;width:24px;height:24px;}#blackout_tools{background-color:#888888;position:fixed;top:0px;left:0px;z-index:999;}</style>');
$('body').append('<div id="blackout_tools"><input type="button" class="color" style="background-color:#000;" onclick="setColor(\'black\')"><input type="button" class="color" style="background-color:#fff;" onclick="setColor(\'white\')"><input type="button" class="color" style="background-color:#FF0000;" onclick="setColor(\'red\')"><input type="button" class="color" style="background-color:#00FF00;" onclick="setColor(\'green\')"><input type="button" class="color" style="background-color:#0000FF;" onclick="setColor(\'blue\')"><input type="button" class="color" style="background-color:#FF1493;" onclick="setColor(\'pink\')"><input type="button" value="Finalize" onclick="apply()" style="display:none"></div>');

$(document).ready(function(){
    $('body').bind("mouseup", function(){
        if (color == "black")
            highlight();
        else if (color == "white")
            highlight();
        else if (color == "red")
            highlight();
        else if (color == "green")
            highlight();
        else if (color == "blue")
            highlight();
        else if (color == "pink")
            highlight();
        else
            alert("Error: " + color + " not found");
    });
});
}

function setColor(value)
{
color = value;
}

function apply()
{
$('.blackout').css('color', '#000');
$('.whiteout').css('color', '#FFF');
$('.redout').css('color', '#F00');
$('.greenout').css('color', '#0F0');
$('.blueout').css('color', '#00F');
$('.pinkout').css('color', '#FF1493');
}
