
/*

 Set Background URL

 */


$(function(){
    $("[bg-url]").each(function(){
        $(this).css("background-image", "url(" + $(this).attr("bg-url") + ")")
    });
});


/*

 Username Duplicate Check Functionality

 */

$("[data-username]").focusout(function(){
    var self = $(this);
    $.ajax({
        url: "/site-extras/username-check",
        data: { username: $(this).val() }
    }).done(function( msg ) {
        self.parent().removeClass("has-success has-error");
        if (msg.result == 0){
            self.parent().addClass("has-success");
        }
        else if(msg.result == 1){
            self.parent().addClass("has-error");
        }
        $(self.attr("data-target")).html(msg.message);
    });
});



/*

 SNS Sharing Functionality

 */

$("[sns]").click(function(){
    var sns = $(this).attr("sns");
    var title = $(this).attr("title");
    sendSns(sns, document.location, title);
});


function sendSns(sns, url, txt)
{
    var o;
    var _url = encodeURIComponent(url);
    var _txt = encodeURIComponent(txt);
    var _br  = encodeURIComponent('\r\n');

    switch(sns)
    {
        case 'facebook':
            o = {
                method:'popup',
                url:'http://www.facebook.com/sharer/sharer.php?u=' + _url
            };
            break;

        case 'twitter':
            o = {
                method:'popup',
                url:'http://twitter.com/intent/tweet?text=' + _txt + '&url=' + _url
            };
            break;

        case 'me2day':
            o = {
                method:'popup',
                url:'http://me2day.net/posts/new?new_post[body]=' + _txt + _br + _url + '&new_post[tags]=epiloum'
            };
            break;

        case 'kakaotalk':
            o = {
                method:'web2app',
                param:'sendurl?msg=' + _txt + '&url=' + _url + '&type=link&apiver=2.0.1&appver=2.0&appid=dev.epiloum.net&appname=' + encodeURIComponent('Epiloum 개발노트'),
                a_store:'itms-apps://itunes.apple.com/app/id362057947?mt=8',
                g_store:'market://details?id=com.kakao.talk',
                a_proto:'kakaolink://',
                g_proto:'scheme=kakaolink;package=com.kakao.talk'
            };
            break;

        case 'kakaostory':
            o = {
                method:'web2app',
                param:'posting?post=' + _txt + _br + _url + '&apiver=1.0&appver=2.0&appid=dev.epiloum.net&appname=' + encodeURIComponent('Epiloum 개발노트'),
                a_store:'itms-apps://itunes.apple.com/app/id486244601?mt=8',
                g_store:'market://details?id=com.kakao.story',
                a_proto:'storylink://',
                g_proto:'package=com.kakao.story'
            };
            break;

        case 'band':
            o = {
                method:'web2app',
                param:'create/post?text=' + _txt + _br + _url,
                a_store:'itms-apps://itunes.apple.com/app/id542613198?mt=8',
                g_store:'market://details?id=com.nhn.android.band',
                a_proto:'bandapp://',
                g_proto:'scheme=bandapp;package=com.nhn.android.band'
            };
            break;

        default:
            alert('지원하지 않는 SNS입니다.');
            return false;
    }

    switch(o.method)
    {
        case 'popup':
            window.open(o.url);
            break;

        case 'web2app':
            if(navigator.userAgent.match(/android/i))
            {
                // Android
                setTimeout(function(){ location.href = 'intent:'+ o.a_proto + o.param + '#Intent;' + o.g_proto + ';end;'}, 100);

            }
            else if(navigator.userAgent.match(/(iphone)|(ipod)|(ipad)/i))
            {
                // Apple
                setTimeout(function(){ location.href = o.a_store; }, 200);
                setTimeout(function(){ location.href = o.a_proto + o.param }, 100);
            }
            else
            {
                alert('이 기능은 모바일에서만 사용할 수 있습니다.');
            }
            break;
    }
}


/*

 Phone Check Functionality

 */

function waitForCode(seconds){
    $("#request-remaining").show();
    $("#request-code-button").hide();
    $("input[name=phone_number]").attr("readonly", "");
    var timer = new Tock({
        countdown: true,
        interval: 100,
        callback: function () {
            var seconds = Math.floor((timer.lap() / 1000) % 60);
            var minutes = Math.floor((timer.lap() / (60 * 1000)) % 60);
            seconds = seconds > 9 ? "" + seconds: "0" + seconds;
            $('#request-remaining').html(minutes+":"+seconds);
        },
        complete: function(){
            resetPhoneField();
        }
    });
    timer.start(seconds*1000);
};
function resetPhoneField(){
    $("#request-remaining").hide();
    $("#request-code-button").show();
    $("input[name=phone_number]").removeAttr("readonly");
    $("#phone_number-form-group .error-container").html("");
    $("#phone_number-form-group").removeClass("has-success has-warning has-error");
}

$(function(){
    var phone_number = $("#id_phone_number").val();
    var button = $("#request-code-button");
    if(phone_number && button && button.hasClass("click")){
        //button.trigger("click");
    }
});

$("#request-code-button").click(function(){
    var no_duplicates = $("input[name=no_duplicates]");
    var phone_number = $("input[name=phone_number]");
    var data;
    if (no_duplicates){
        data = {
            phone_number : phone_number.val(),
            no_duplicates: no_duplicates.val()
        };
    }
    else{
        data = {
            phone_number : phone_number.val()
        };
    }

    $.ajax({
        url: "/site-extras/send-code",
        type: "POST",
        data: data
    }).done(function(data) {
        resetPhoneField();
        $("#phone_number-form-group .error-container").html("<label class='label label-danger'>"+data.result+"</label>");
        if (data.error_code == 0){
            $("#phone_number-form-group").addClass("has-success");
            waitForCode(data.remaining);
        }
        else if (data.error_code == 1){
            $("#phone_number-form-group").addClass("has-warning");

            waitForCode(data.remaining);
        }
        else if (data.error_code == 2){
            $("#phone_number-form-group").addClass("has-error");
        }
    });
});