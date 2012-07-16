$(document).ready(function() {
    var v = document.getElementById("uservideo");
    var gum = null;
    if(navigator.getUserMedia)
      gum = function(success, fallback) {navigator.getUserMedia({video: true, audio: false}, success, fallback);};
    else if(navigator.webkitGetUserMedia)
      gum = function(success, fallback) {navigator.webkitGetUserMedia({video: true, audio: false}, success, fallback);};

    gum(function(stream) {
      if(window.webkitURL)
        stream = window.webkitURL.createObjectURL(stream);
      v.src = stream;

      var sn = document.getElementById("snapshot");
      $("#take_picture").click(function() {
        $(sn).show();
        $(v).hide();
        var ctx = sn.getContext("2d");
        ctx.drawImage(v, 0, 0, v.videoWidth, v.videoHeight);
        $(this).hide();
        $("#save_picture, #cancel_picture").show();
      });
      function reset() {
        $("#take_picture").show();
        $(v).show();
        $(sn).hide();
        $("#save_picture, #cancel_picture").hide();
      }
      $("#save_picture").click(function() {
        $.post("/post_pic", {
          url: sn.toDataURL()
        }, function() {alert("Uploaded!");});
        reset();
      });
      $("#cancel_picture").click(function() {
        $("#take_picture").show();
        reset();
      });

    }, function(e) {
      alert("We couldn't talk to your webcam. Sorry :(");
    });
});
