var url             = "https://pokyfriends.com/tool/bk-mario-maker/";
var key             = location.search.split('key=')[1];
var mode            = "toggle";
var game            = "smb";
var game_max        = 4;
var theme_max       = 6;
var element_max     = 60;
var autoscroll_max  = 4;
var featured_max    = 4;

var clock_interval  = window.setInterval(update_clock, 1000);

var game_decoder    = "M3WN";
var theme_decoder   = "GUWHAC";
var hex             = "0123456789ABCDEF";

$(document).ready(function(){
    $(".game-choice").click(function (){
        $(this).toggleClass("gray");
        if (! $(this).hasClass("gray"))
        {
            game = $(this).data("game");
            reload_tiles();
        }
        else
        {
            $(".game-choice").each(function (){
                if (! $(this).hasClass("gray"))
                {
                    game = $(this).data("game");
                    reload_tiles();
                    return;
                }
            });
        }
        generate_key(true);
    });

    $(".theme-choice").click(function (){
        $(this).toggleClass("gray");
        generate_key(true);
    });

    $(".element-choice").click(function (){
        if (mode == "toggle")
        {
            $(this).toggleClass("gray");
            if ($(this).hasClass("gray"))
                validate_featured();
        }
        else
        {
            $(this).removeClass("gray");
            var src = $(this).find("img").attr("src");
            $(".featured-choice").find(".selected").attr("src", src);
            $(".featured-choice").find(".selected").removeClass("selected");
            mode = "toggle";
        }
        generate_key(true);
    });

    $(".autoscroll-choice").click(function (){
        $(this).toggleClass("gray");
        generate_key(true);
    });

    $(".featured-choice").click(function (){
        if (mode == "toggle")
        {
            mode = "featured";
            $(this).find("img").addClass("selected");
        }
        else
        {
            mode = "toggle";
            $(".featured-choice").find("img").removeClass("selected");
        }
        generate_key(true);
    });

    $(".control-button").click(function (){
        action = $(this).text();

        if (action == "Everything")
            randomize_all(true);
        else if (action == "Randomize Game")
            randomize_game(true);
        else if (action == "Randomize Theme")
            randomize_theme(true);
        else if (action == "Randomize Elements")
            randomize_elements(true);
        else if (action == "Randomize Autoscroll")
            randomize_autoscroll(true);
        else if (action == "Randomize Featured")
            randomize_featured(true);
        else if (action == "Reset")
            reset(true);
    });

    $("#tileset").change(function (){
        game = $(this).val();
        reload_tiles();
    });

    $("#upload-date").change(function (){
        generate_key(true);
    });

    $("#upload-time").change(function (){
        generate_key(true);
    });

    $("#link-input").click(function (){ $(this).select(); });

    if (key)
        load();
    else
        randomize_all(true);
});

function reset(make_key)
{
    $(".game-choice").removeClass("gray");
    $(".theme-choice").removeClass("gray");
    $(".element-choice").removeClass("gray");
    $(".autoscroll-choice").removeClass("gray");
    $("#f1").removeClass("gray");
    $("#f2").removeClass("gray");
    $("#f3").removeClass("gray");
    $("#f4").removeClass("gray");
    generate_key(make_key);
}

function randomize_all(make_key)
{
    randomize_game(false);
    randomize_theme(false);
    randomize_elements(false);

    // 90% chance of no autoscroll on initial load
    if ((Math.floor(Math.random() * 10) + 1) != 10)
    {
        $(".autoscroll-choice").each(function(){
            $(this).addClass("gray");
        });
        $(".autoscroll-choice:first").removeClass("gray");
    }
    else
    {
        randomize_autoscroll(false);
    }

    randomize_featured(false);
    generate_key(make_key);
    update_clock();
}

function update_clock()
{
    var date = new Date();
    var date_text = date.getFullYear() + "-" + ("0" + (date.getMonth()+1)).slice(-2) + "-" + ("0" + date.getDate()).slice(-2);
    var h = ("0" + date.getHours()).slice(-2);
    var m = ("0" + date.getMinutes()).slice(-2);
    var s = ("0" + date.getSeconds()).slice(-2);
    $("#clock").text(h + ":" + m + ":" + s);
    $("#date").text(date_text);
    if ($("#date").text() == $("upload-date").val())
    {
        if ($("#clock").text() > $("upload-time").val())
        {
            $("#clock").css("color", "red");
            $("#date").css("color", "red");
        }
    }
}

function randomize_game(make_key)
{
    var choice = Math.floor(Math.random() * game_max) + 1;
    var count = 1;
    $(".game-choice").each(function (){
        if (count != choice)
        {
            $(this).addClass("gray");
        }
        else
        {
            $(this).removeClass("gray");
            game = $(this).data("game");
        }
        count++;
    });
    reload_tiles();
    generate_key(make_key);
}

function randomize_theme(make_key)
{
    var choice = Math.floor(Math.random() * theme_max) + 1;
    var count = 1;
    $(".theme-choice").each(function (){
        if (count != choice)
        {
            $(this).addClass("gray");
        }
        else
        {
            $(this).removeClass("gray");
        }
        count++;
    });
    generate_key(make_key);
}

function randomize_elements(make_key)
{
    count = 1;
    $(".element-choice").each(function (){
        if (count <= 4)
        {
            $(this).removeClass("gray");
        }
        else
        {
            var choice = Math.floor(Math.random() * 3) + 1;
            if (choice == 3)
            {
                $(this).addClass("gray");
            }
            else
                $(this).removeClass("gray");
        }
        count++;
    });

    validate_featured();
    generate_key(make_key);
}

function randomize_autoscroll(make_key)
{
    var choice = Math.floor(Math.random() * autoscroll_max) + 1;
    var count = 1;
    $(".autoscroll-choice").each(function (){
        if (count != choice)
        {
            $(this).addClass("gray");
        }
        else
        {
            $(this).removeClass("gray");
        }
        count++;
    });
    generate_key(make_key);
}

function randomize_featured(make_key)
{
    var choices = [];
    $(".element-choice").each(function (){
        if (! $(this).hasClass("gray"))
        {
            var id = $(this).find("img").attr("id");
            var skip = ["1-1", "1-2", "1-3", "1-4"];
            if (skip.indexOf(id) == -1)
                choices.push(id);
        }
    });

    for (var i = choices.length - 1; i > 0; i--) {
        var j = Math.floor(Math.random() * (i + 1));
        var temp = choices[i];
        choices[i] = choices[j];
        choices[j] = temp;
    }

    for (var x = 1; x <= 4; x++)
    {
        $("#f"+x).attr("src", "/static/tool/bk-mario-maker/" + game + "/" + choices[x] + ".png");
        $("#f"+x).attr("alt", choices[x]);
    }
    generate_key(make_key);
}

function validate_featured()
{
    var featured = [];
    featured.push($("#f1").attr("src").replace(".png", "").split("/")[1]);
    featured.push($("#f2").attr("src").replace(".png", "").split("/")[1]);
    featured.push($("#f3").attr("src").replace(".png", "").split("/")[1]);
    featured.push($("#f4").attr("src").replace(".png", "").split("/")[1]);

    $(".element-choice").each(function (){
        if ($(this).hasClass("gray"))
        {
            id = $(this).find("img").attr("id");
            var index = featured.indexOf(id);
            if (index != -1)
            {
                for (var x = 0; x < 4; x++)
                {
                    if (featured[x] == id)
                    {
                        $("#f"+(x+1)).attr("src", "blank-featured.png")
                    }
                }
            }
        }
    });
    return true;
}

function generate_key(make_key)
{
    if (! make_key)
        return false;

    var key = "";

    // Game
    var idx = 0;
    $(".game-choice").each(function (){
        if (! $(this).hasClass("gray"))
            key += game_decoder[idx];
        idx += 1;
    });

    key += "-"

    // Theme
    var idx = 0;
    $(".theme-choice").each(function (){
        if (! $(this).hasClass("gray"))
            key += theme_decoder[idx];
        idx += 1;
    });

    key += "-"

    // Elements
    var idx = 0;
    var component = 0;
    $(".element-choice").each(function (){
        if (! $(this).hasClass("gray"))
        {
            bits = Math.pow(2,idx);
            component += bits;
        }
        idx += 1;

        if (idx == 4)
        {
            idx = 0;
            key += "" + hex[component];
            component = 0;
        }

    });
    key += "" + hex[component]; // Final iteration
    key = key.slice(0,-1) + "-";

    // Autoscroll
    var idx = 0;
    var component = 0;
    $(".autoscroll-choice").each(function (){
        if (! $(this).hasClass("gray"))
        {
            bits = Math.pow(2,idx);
            component += bits;
        }
        idx += 1;

        if (idx == 4)
        {
            idx = 0;
            key += "" + hex[component];
            component = 0;
            return true;
        }
    });

    key += "-";

    // Featured
    var idx = 0;
    key += $("#f1").attr("alt").replace("-", "") + ":";
    key += $("#f2").attr("alt").replace("-", "") + ":";
    key += $("#f3").attr("alt").replace("-", "") + ":";
    key += $("#f4").attr("alt").replace("-", "");

    key += "-";

    // Clock
    var clock = $("#clock").text();
    var u_date = $("#upload-date").val();
    var upload = $("#upload-time").val();
    var input = u_date + "T" + upload;
    var date = new Date(input);
    var time = date.getTime() / 1000;

    if (isNaN(time))
        time = "X";

    key += time;

    $("#link-input").val(url + "?key=" + key);
    $("#link-text").attr("href", (url + "?key=" + key));
    //$("#twitter").attr("href", "https://twitter.com/intent/tweet?url="+url+"?key"+key+"&hashtags=BKMM");
    $("#debug").html(key);
}

function load()
{
    var components = key.split("-");
    var games = components[0];
    var themes = components[1];
    var elements = components[2];
    var autoscroll = components[3];
    var featured = components[4];
    var due = components[5];
    // Haha I wrote my binary left to right, no wonder I was having problems decoding it
    var hex_dict = {"0":"0000", "1":"1000", "2":"0100", "3":"1100", "4":"0010", "5":"1010", "6":"0110", "7":"1110", "8":"0001", "9":"1001", "A":"0101", "B":"1101", "C":"0011", "D":"1011", "E":"0111", "F":"1111"};

    // Game
    var idx = 0;
    $(".game-choice").each(function (){
        if (idx == 0 && games.indexOf("M") == -1)
            $(this).addClass("gray");
        else
            game = "smb";
        if (idx == 1 && games.indexOf("3") == -1)
            $(this).addClass("gray");
        else
            game = "smb3";
        if (idx == 2 && games.indexOf("W") == -1)
            $(this).addClass("gray");
        else
            game = "smw";
        if (idx == 3 && games.indexOf("N") == -1)
            $(this).addClass("gray");
        else
            game = "nsmb";
        idx += 1;
    });

    reload_tiles();

    // Theme
    var idx = 0;
    $(".theme-choice").each(function (){
        if (idx == 0 && themes.indexOf("G") == -1)
            $(this).addClass("gray");
        if (idx == 1 && themes.indexOf("U") == -1)
            $(this).addClass("gray");
        if (idx == 2 && themes.indexOf("W") == -1)
            $(this).addClass("gray");
        if (idx == 3 && themes.indexOf("H") == -1)
            $(this).addClass("gray");
        if (idx == 4 && themes.indexOf("A") == -1)
            $(this).addClass("gray");
        if (idx == 5 && themes.indexOf("C") == -1)
            $(this).addClass("gray");
        idx += 1;
    });

    // Elements
    var idx = 0;
    var component = 0;
    element_bits = "";

    for (var x = 0; x < elements.length; x++)
    {
        var temp = hex_dict[elements[x]];
        element_bits += temp;
    }

    var idx = 0;
    $(".element-choice").each(function (){
        if (element_bits[idx] == "0")
            $(this).addClass("gray");
        idx++;
    });

    // Autoscroll
    var autoscroll_bits = hex_dict[autoscroll];

    var idx = 0;
    $(".autoscroll-choice").each(function (){
        if (autoscroll_bits[idx] == "0")
            $(this).addClass("gray");
        idx++;
    });

    // Featured
    var featured_array = featured.split(":");

    var idx = 0;

    for (var x = 1; x <= 4; x++)
    {
        var tile = featured_array[x-1];
        tile = tile.slice(0,1) + "-" + tile.slice(1);
        $("#f"+x).attr("src", "/static/tool/bk-mario-maker/" + game + "/" + tile + ".png");
        $("#f"+x).attr("alt", tile);
    }

    // Clock
    if (due != "NaN" && due != "X")
    {
        var date = new Date(due*1000);
        var h = ("0" + date.getHours()).slice(-2);
        var m = ("0" + date.getMinutes()).slice(-2);
        var s = ("0" + date.getSeconds()).slice(-2);
        $("#upload-time").val(h + ":" + m + ":" + s);
        var y = date.getFullYear();
        var m = ("0" + (date.getMonth()+1)).slice(-2);
        var d = ("0" + date.getDate()).slice(-2);
        $("#upload-date").val(y + "-" + m + "-" + d);
    }

    $("#link-input").val(url + "?key=" + key);
    $("#link-text").attr("href", (url + "?key=" + key));
    //$("#twitter").attr("href", "https://twitter.com/intent/tweet?url="+url+"?key"+key+"&hashtags=BKMM");
}

function reload_tiles()
{
    $("#tileset").val(game);
    $(".element-choice").each(function (){
        $(this).find("img").attr("src", "/static/tool/bk-mario-maker/" + game + "/" + $(this).find("img").attr("alt") + ".png");
    });

    $(".featured-choice").each(function (){
        $(this).find("img").attr("src", "/static/tool/bk-mario-maker/" + game + "/" + $(this).find("img").attr("alt") + ".png");
    });
}
