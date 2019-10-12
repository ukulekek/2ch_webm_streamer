//saves info about video
function saveVideo(index){
    video = $('#videoArea')
    localStorage.setItem("activeVideo", index);
    volume = video.get(0).volume;
    if(volume != undefined){
        volume = localStorage.setItem("volume", volume.toFixed(4));
    }
}

function isLiVisible(elem)
{
    var listViewTop = $('#playlist').position().top;
    var listViewBot = listViewTop + $('#playlist').height();

    var elemTop = $(elem).position().top;
    var elemBottom = elemTop + $(elem).outerHeight();

    return ((elemBottom <= listViewBot) && (elemTop >= listViewTop));
}

//bind click on video name to play it
$('#playlist li').each(function(){
  $(this).click(function(){
    var curUrl = $(this).attr("src");
    $('#videoArea').attr("src",curUrl)
    $('#videoArea').attr("autoplay","autoplay")

    $('#playlist > li[active]').removeAttr('active');
    $(this).attr('active','');
    //save active video to local storage
    saveVideo($(this).index());
  });
});


//scroll playlist
function scrollPlaylist(offset, down = 1){
  if(down == 0){
    offset = -offset
  }
  $('#playlist').scrollTop($('#playlist').scrollTop() + offset);
}


// play next/previous video
function playVideo(next=1){
  var activeVideo = $("#playlist > li[src='"+$("#videoArea").attr("src")+"']")
  var video;
  if(next == 1){
    video = activeVideo.next();
  }
  else{
    video = activeVideo.prev();
  }
  if(video.length == 0)
  	return;

  //scroll playlist
  if(!isLiVisible(video)){
    var heightOffset = video.outerHeight();
    scrollPlaylist(heightOffset*1.5, next);
  }

  $('#videoArea').attr("src", video.attr("src"))
  $('#videoArea').attr("autoplay","autoplay")

  video.attr('active','');
  activeVideo.removeAttr('active');
  //save active Video to local storage
  saveVideo(video.index());
};


//play next video when current is ended
$("#videoArea").on('ended',function(){ playVideo(1); });


$(function(){
  $("#left svg").click(function(){
    playVideo(0)
  });
  $("#right svg").click(function(){
    playVideo(1)
  });
});


//load last played video
$(function(){
    var videoIndex = localStorage.getItem("activeVideo");
    var volume = localStorage.getItem("volume");
    if(videoIndex != undefined){
        var video = $('#playlist > li:nth-child(' + (parseInt(videoIndex) + 1) + ')')
        //scroll to choosen video
        var offset = $('#playlist > li').first().position().top;
        $('#playlist').scrollTop(video.position().top - offset);
        //set previous volume
        if(volume != "undefined"){
            $('#videoArea').get(0).volume = parseFloat(volume);
        }
        //click on video and pause it
        video.click();
        $('#videoArea').get(0).pause();
        $('#videoArea').get(0).muted = false;
    }
})
