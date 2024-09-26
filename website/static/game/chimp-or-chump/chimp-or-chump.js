canvas = 0;
game = 0;

//Game variables
mode = "idle";
x = 0;
y = 0;
locations = [];
target = 1;
maxnum = 5;

//Stats
tries = 1;
times = [0, 0, 0, 0, 0, 0];
victory = false;
sound = 1;

//Sounds
snd_yes = new Audio("/static/game/chimp-or-chump/sounds/boop.ogg");

function play()
{
    if (sound == 1)
        snd_yes.play();
}

var start = "";

var start = new Image();
start.src = 'images/start.png';
start.onload = function() {
    //Draw original to palette canvas
    var canvas = document.getElementById('game');
    var game = canvas.getContext('2d');
    game.drawImage(start, 2*80, 4*60);
  };

$(document).ready(function() {
    canvas = document.getElementById("game");
    game = canvas.getContext('2d');

    //Make graphics
    tile1 = document.getElementById("i1");
    tile2 = document.getElementById("i2");
    tile3 = document.getElementById("i3");
    tile4 = document.getElementById("i4");
    tile5 = document.getElementById("i5");
    tile6 = document.getElementById("i6");
    tile7 = document.getElementById("i7");
    tile8 = document.getElementById("i8");
    tile9 = document.getElementById("i9");
    tile10 = document.getElementById("i10");

    start = document.getElementById("istart");
    gameover = document.getElementById("igameover");
    cont = document.getElementById("icont");
    statsframe = document.getElementById("iframe");


    game.drawImage(start, 2*80, 4*60);

    //Dimensions 80x60 (whole grid is 8x8)

    $('#soundtoggle').click(function (e){
    sound = sound * -1;
    if (sound == 1)
        play();
    });

    $('#game').click(function (e){
        x = parseInt((e.pageX - this.offsetLeft) / 80);
        y = parseInt((e.pageY - this.offsetTop) / 60);
        $('#debugCoords').html(x +  " / " + y);

        if (mode == "idle")
        {
            if ((x >= 2 && x <= 5) && (y == 4))
            {
                setup(maxnum);

                play();
            }
        }
        else if (mode == "play")
        {


            //Did you click the target?
            if ((x == locations[target-1][0]) && (y == locations[target-1][1]))
            {
                play();
                //Clear the tile
                locations[target-1] = [-1, -1];
                game.fillStyle = "#000";
                game.fillRect(x*80, y*60, 80, 60);

                //Update the target
                target += 1;

                //Did you just start?
                if (target == 2)
                {
                    hide();
                }

                //Did you win?
                if (target == maxnum+1)
                {
                    play();
                    clear()
                    foo = new Date;
                    end = foo.getTime(); // Returns milliseconds since the epoch
                    times[maxnum-5] = (end - begin) / 1000;
                    if (maxnum < 10)
                    {
                        game.drawImage(cont, 2*80, 4*60);
                        maxnum+=1;
                        mode = "idle";
                    }
                    else
                    {
                        victory = true;
                        gameOver();
                    }
                }
            }
            else
            {
                if (isTile())
                {
                    play();
                    foo = new Date;
                    end = foo.getTime(); // Returns milliseconds since the epoch
                    times[maxnum-5] = (end - begin) / 1000;
                    gameOver();
                }
            }
        }

    });
});

    function setup(maxnum)
    {
        //Get 10 pairs of coordinates
        locations = new Array(maxnum);
        possible = makePossible();
        clear()
        getNums(maxnum);

        $('#debugLocs').html("{"+locations[0]+"} {"+locations[1]+"} {"+locations[2]+"} {"+locations[3]+"} {"+locations[4]+"} {"+locations[5]+"} {"+locations[6]+"} {"+locations[7]+"} {"+locations[8]+"} {"+locations[9]+"}");

        //Clear button
        game.fillStyle = "#000";
        game.fillRect(160, 180, 320, 120);

        //Draw the 10 tiles
        tile = [tile1, tile2, tile3, tile4, tile5, tile6, tile7, tile8, tile9, tile10]
        for (var count = 0; count < locations.length; count++)
        {
            game.drawImage(tile[count], locations[count][0]*80, locations[count][1]*60);
        }

        //Start playing!
        target = 1;
        mode = "play";

        foo = new Date;
        begin = foo.getTime(); // Returns milliseconds since the epoch
    }

function getNums()
{
    for (var count = 0; count < maxnum; count++)
    {
        index = Math.floor(Math.random()*possible.length);

        locations[count] = possible[index];
        possible.splice(index,1);
    }
}

function makePossible()
{
    ret = []
    for (possX = 0; possX < 8; possX++)
    {
        for (possY = 0; possY < 8; possY++)
            ret.push([possX, possY]);
    }
    return ret;
}

function isTile()
{
    for (pos = 0; pos < locations.length; pos++)
    {
        a = locations[pos][0];
        b = locations[pos][1];
        //alert(a + " " + b + " / " + x + " " + y);
        if ((a == x) && (b == y))
        {
            return true;
        }
    }
    return false;
}

function hide()
{
    game.fillStyle = "#0f0";
    for (pos = 0; pos < locations.length; pos++)
    {
        a = locations[pos][0] * 80;
        b = locations[pos][1] * 60;
        game.fillRect(a,b,80,60);
    }
}

function gameOver()
{
    clear();
    mode = "idle"


    game.drawImage(gameover, 160, 180);
    game.drawImage(start, 160, 240);
    game.drawImage(statsframe, 160, 0);

    game.font="18pt Lucida Console";
    game.textAlign = "center";
    game.fillStyle = "#00ffff";
    if (victory)
    {
        game.fillText("CONGRATULATIONS!", 310, 25);
        mode = "victory";
    }
    game.textAlign = "right";
    game.fillText(tries, 473, 172);

    game.font="14pt Lucida Console";
    game.textAlign = "left";
    if (maxnum == 5)
        game.fillStyle = "#ff0000";
    if (times[0] != 0)
        game.fillText(times[0], 190, 79);
    if (maxnum == 6)
        game.fillStyle = "#ff0000";
    if (times[1] != 0)
        game.fillText(times[1], 190, 97);
    if (maxnum == 7)
        game.fillStyle = "#ff0000";
    if (times[2] != 0)
        game.fillText(times[2], 190, 115);
    if (maxnum == 8)
        game.fillStyle = "#ff0000";
    if (times[3] != 0)
        game.fillText(times[3], 341, 79);
    if (maxnum == 9)
        game.fillStyle = "#ff0000";
    if (times[4] != 0)
    game.fillText(times[4], 341, 97);
    if ((maxnum == 10 ) && (mode != "victory"))
        game.fillStyle = "#ff0000";
    if (times[5] != 0)
    game.fillText(times[5], 341, 115);

    totalTime = Math.round((times[0] + times[1] + times[2] + times[3] + times[4] + times[5])*Math.pow(10,3))/Math.pow(10,3)
    game.font="18pt Lucida Console";
    game.textAlign="left";
    game.fillText(totalTime, 165, 172);

    times = [0,0,0,0,0,0];
    maxnum = 5;
    tries++;

    if (victory = true)
    {
        mode = "idle";
        tries = 1;
    }
}

function clear()
{
    game.fillStyle = "#000";
    game.fillRect(0,0,640,480);
}
