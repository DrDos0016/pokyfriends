"use strict";
var canvas = document.getElementById("canvas");
var ctx = canvas.getContext("2d");

if (window.location.href.indexOf("?") != -1)
    var song = window.location.href.split("?")[1];
else
    var song = "gggdeedbbccdxxdgggdffgxbbccd";
var played = "";
var staff_start = -1;

var scroll_amount = 9;
var selected = "c";
var entities = [];

var curtain_call = null;
var curtains = -480;

class Entity
{
    constructor(img, x, y, entity="entity", width=1, height=1)
    {
        this.image = document.getElementById("gfx-"+img);
        this.tile = [x, y];
        this.x = x * 32;
        this.y = y * 32;
        this.width = width;
        this.height = height;
        this.tag = entity;
    }

    render()
    {
        ctx.drawImage(this.image, this.x, this.y);
    }

    click(idx)
    {
        return false;
    }

    play()
    {
        return false;
    }
}

class Note_Button extends Entity
{
    constructor(img, x, y)
    {
        super(img, x, y, "note-"+img);
        this.note = img;
        this.sound = document.getElementById("sfx-"+img);
    }

    click(idx)
    {
        $("audio").each(function(){
            this.pause(); // Stop playing
            this.currentTime = 0; // Reset time
        });
        this.sound.play();
        selected = this.note;
        return true;
    }
}

class Scroll_Button extends Entity
{
    constructor(img, x, y)
    {
        super(img, x, y, "scroll-"+img, 1, 2);
        this.direction = img;
    }

    click(idx)
    {
        if (this.direction == "back")
        {
            staff_start -= scroll_amount;
        }
        else
        {
            staff_start += scroll_amount;
        }

        if (staff_start > song.length)
            staff_start = staff_start - scroll_amount;
        staff_start = Math.max(staff_start, -1);

        render_song();
    }
}

class Player extends Entity
{
    constructor(x, y)
    {
        super("player", 9, 6, "player");
    }

    move(key)
    {
        var old_tx = this.tile[0];
        var old_ty = this.tile[1];
        var tile_x = this.tile[0] - (key == "a")*1 + (key == "d")*1;
        var tile_y = this.tile[1] - (key == "w")*1 + (key == "s")*1;

        if (tile_x < 0 || tile_x > 19 || tile_y < 0 || tile_y > 11)
            return false;

        ctx.drawImage(document.getElementById("gfx-wood"), this.x, this.y);

        // If a note tile is on your old tile, redraw it
        var idx = entity_at(old_tx, old_ty, "tile");
        if (idx != -1 && entities[idx].tag != "player")
        {
            entities[idx].render();
        }

        this.tile = [tile_x, tile_y]
        this.x = tile_x * 32;
        this.y = tile_y * 32

        // If a note tile is on your new tile, play it
        var idx = entity_at(tile_x, tile_y, "tile");
        if (idx != -1)
        {
            entities[idx].play();
        }

        this.render();
        return true;
    }

    click(idx)
    {
        return true;
    }
}

class Note_Tile extends Entity
{
    constructor(img, x, y)
    {
        super(img, x, y, "tile-"+img);
        this.note = img;
        this.sound = document.getElementById("sfx-"+img);
    }

    click(idx)
    {
        if (played.length != 0 && played.indexOf("-") == -1)
            return false;
        ctx.drawImage(document.getElementById("gfx-wood"), this.x, this.y);
        entities.splice(idx, 1);
        return true;
    }

    play(idx)
    {
        if (this.note == song[played.length])
        {
            played += this.note;

            // Check if the song is completed
            if (played.length == song.length && played.indexOf("-") == -1)
            {
                entities = [];
                window.setTimeout(victory, 1500);
            }

            // If the next note is rest, auto-hit it
            while (true)
            {
                if (song[played.length] == "x")
                    played += "x";
                else
                    break;
            }


            if (played.length == staff_start+scroll_amount)
            {
                click_tile(19,12);
            }
        }
        else
        {
            // Erase non-practice notes
            //played = "";
            var reset = "";
            for (var temp = 0; temp < played.length; temp++)
            {
                if (played[temp] == "-")
                    reset += "-";
                else
                    break;
            }
            played = reset;

            var offset = played.length % scroll_amount; // Offset for autoscrolling
            /*
            console.log("OFFSET", offset);
            if (offset)
                staff_start = -1 + (offset * scroll_amount) + scroll_amount;
            else
            */
            staff_start = -1;
            click_tile(0,12);
        }
        $("audio").each(function(){
            this.pause(); // Stop playing
            this.currentTime = 0; // Reset time
        });
        this.sound.play();
        render_song();
        return true;
    }
}


function render_entities()
{
    for (var idx in entities)
    {
        entities[idx].render();
    }
}

function render_song()
{
    // Background layer

    // First tile
    if (staff_start == -1)
        ctx.drawImage(document.getElementById("gfx-staff"), 32, 384);
    else
        ctx.drawImage(document.getElementById("gfx-bar"), 32, 384);

    for (var temp = 1; temp < 17; temp++)
        ctx.drawImage(document.getElementById("gfx-bar"), 32*temp+32, 384);

    // Last tile
    if ((staff_start + 18) >= song.length)
        ctx.drawImage(document.getElementById("gfx-end"), 576, 384);
    else
        ctx.drawImage(document.getElementById("gfx-bar"), 576, 384);

    var note_offsets = {"a":15, "b":20, "c":-10, "d":-5, "e":0, "f":5, "g":10}
    var x = 40;
    for (var count = 0; count < 18; count++)
    {
        var idx = staff_start + count;
        if (idx >= 0 && idx < song.length)
        {
            var note = song[idx];
            if (note != "x") // Don't render a rest
            {
                if (played.length > idx) // It's a played note
                {
                    ctx.drawImage(document.getElementById("gfx-note-played"), x, 417-note_offsets[note]);
                }
                else  // It's an unplayed note
                {
                    ctx.drawImage(document.getElementById("gfx-note-"+note), x, 417-note_offsets[note]);
                }
            }
        }
        x += 32;
    }
}

function entity_at(x, y, tagged="")
{
    for (var idx in entities)
    {
        if (entities[idx].tile[0] == x && entities[idx].tile[1] == y)
        {
            if (tagged == "")
                return idx;
            else if (tagged == entities[idx].tag.slice(0,tagged.length))
            {
                return idx;
            }
        }
    }
    return -1;
}

function click_tile(x, y)
{
    // Practice mode
    if ((x >= 1 && x <= 18) && (y >= 12 && y <= 13))
    {
        played = "";
        var range = staff_range();
        var buffer = "";

        while (buffer.length < (staff_start + x-1))
        {
            buffer += "-";
        }
        played = buffer;
        render_song();
    }


    // Regular entity check
    var matched = false;
    for (var idx in entities)
    {

        if ((x >= (entities[idx].tile[0]) && (x <= (entities[idx].tile[0] + entities[idx].width - 1))) && (y >= (entities[idx].tile[1]) && (y <= (entities[idx].tile[1] + entities[idx].height - 1))))
        {
            matched = entities[idx].click(idx);
        }
    }
    if (! matched && selected && x <= 19 && y <= 11) // Place a note tile
    {
        if (played.length != 0 && played.indexOf("-") == -1)
            return false;
        var temp = new Note_Tile(selected, x, y);
        entities.push(temp);
        $("audio").each(function(){
            this.pause(); // Stop playing
            this.currentTime = 0; // Reset time
        });
        entities[entities.length - 1].sound.play();
        entities[entities.length - 1].render();
    }
}

function staff_range()
{
    //console.log("STAFF RANGE IS FROM SONG IDX", staff_start, "TO", staff_start+scroll_amount);
    return [staff_start, staff_start+scroll_amount];
}

function victory()
{
    console.log("You win!");
    $("audio").each(function(){
        this.pause(); // Stop playing
        this.currentTime = 0; // Reset time
    });
    document.getElementById("sfx-applause").play();

    //curtain_call = setInterval(curtain, 30);
}

function curtain()
{
    ctx.drawImage(document.getElementById("gfx-curtain"),0,curtains);
    curtains += 5;
    if (curtains >= 0)
    {
        window.clearInterval(curtain_call);
    }
}

$(window).bind("load", function() {

    // Create the note buttons
    ctx.fillRect(0,416,640,64);
    var temp = new Note_Button("a", 0, 14);
    entities.push(temp);
    var temp = new Note_Button("b", 1, 14);
    entities.push(temp);
    var temp = new Note_Button("c", 2, 14);
    entities.push(temp);
    var temp = new Note_Button("d", 3, 14);
    entities.push(temp);
    var temp = new Note_Button("e", 4, 14);
    entities.push(temp);
    var temp = new Note_Button("f", 5, 14);
    entities.push(temp);
    var temp = new Note_Button("g", 6, 14);
    entities.push(temp);

    // Render song
    render_song();

    // Create scroll buttons
    var temp = new Scroll_Button("back", 0, 12);
    entities.push(temp);
    var temp = new Scroll_Button("forward", 19, 12);
    entities.push(temp);

    // Create Player
    var temp = new Player(9, 6);
    entities.push(temp);


    // Render Entities
    render_entities();

    // Bind Keys
    $(window).keyup(function (e){
        //console.log(e.key);
        var key = e.key;
        switch (key)
        {
            case "w":
            case "a":
            case "s":
            case "d":
            {
                for (var idx in entities)
                {
                    if (entities[idx].tag == "player")
                    {
                        entities[idx].move(key);
                        break;
                    }
                }
                break;
            }
            case "q":
            {
                click_tile(0,12);
                break;
            }
            case "e":
            {
                click_tile(19,12);
                break;
            }
            case "1":
            case "2":
            case "3":
            case "4":
            case "5":
            case "6":
            case "7":
            {
                click_tile(parseInt(key)-1,14);
                break;
            }
            case "r":
            {
                staff_range();
                break;
            }
        }
    });

    $("#loading").hide();
    $("#canvas").show();

    $("#canvas").click(function (e){
        var x = parseInt((e.pageX - this.offsetLeft) / 32);
        var y = parseInt((e.pageY - this.offsetTop) / 32);
        click_tile(x, y);
    });
});
