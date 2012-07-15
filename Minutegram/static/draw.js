var gImage = null;
function draw() {
    var image_url = document.getElementById("image_url").value;
    gImage = new Image();
    gImage.onload = draw_onload;
    gImage.src = image_url;
}
function draw_onload() {
    var canvas = document.getElementById("canvas"),
        ctx = canvas.getContext("2d");
    var canvas_r = document.getElementById("canvas_render"),
        ctx_r = canvas_r.getContext("2d");

    var scale = Math.min(gImage.width / canvas.width, gImage.height / canvas.height);
    var width = canvas.width, height = canvas.height;
    if(gImage.width > gImage.height)
        height /= scale;
    else
        width /= scale;
    ctx.drawImage(gImage, (canvas.width - width) / 2, (canvas.height - height) / 2, width, height);

    ctx.fillStyle = "rgba(255,255,255,0.5)";
    ctx.fillRect(0, 0, canvas.width, canvas.height);

    ctx.fillStyle = "black";
    ctx.beginPath();
    ctx_r.fillStyle = "black";
    ctx_r.beginPath();

    var x, y;

    canvas.onmousedown = function(e) {
        x = e.clientX - canvas.offsetLeft;
        y = e.clientY - canvas.offsetTop;
        ctx.moveTo(x, y);
        ctx_r.moveTo(x, y);
    }

    canvas.onmouseup = function(e) {
        x = y = null;
    }

    canvas.onmousemove = function(e) {
        if (x == null || y == null) {
            return;
        }
        x = e.clientX;
        y = e.clientY;
        x -= canvas.offsetLeft;
        y -= canvas.offsetTop;

        ctx.lineTo(x, y);
        ctx.stroke();
        ctx.moveTo(x, y);

        ctx_r.lineTo(x, y);
        ctx_r.stroke();
        ctx_r.moveTo(x, y);
    }
    canvas.onmouseout = function(e) {x = y = null;}

    var output = document.getElementById("imageresult");
    setInterval(function() {
        output.value = canvas_r.toDataURL();
    }, 1500);
};
