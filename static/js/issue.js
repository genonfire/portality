function onKeyPress(e, search_range, nolook) {
    if (e.keyCode == 13) {
        e.preventDefault();
        search(search_range, nolook);
    }
}

function thumb_down(id) {
    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            xhr.setRequestHeader("X-CSRFToken", $("input[name=csrfmiddlewaretoken]").val());
        }
    });
    $.ajax({
        type: "POST",
        url: "/api/thumb_down/",
        data: {
            id: id
        },
        success: function(data) {
            tagname = '#thumb_down_msg' + id;
            $(tagname).html(data[0]);
        },
        error: function(data) {
            tagname = '#thumb_message' + id;
            $(tagname).html(' 이미 눌렀습니다.');
        }
    });
}

function thumb_up(id) {
    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            xhr.setRequestHeader("X-CSRFToken", $("input[name=csrfmiddlewaretoken]").val());
        }
    });
    $.ajax({
        type: "POST",
        url: "/api/thumb_up/",
        data: {
            id: id
        },
        success: function(data) {
            tagname = '#thumb_up_msg' + id;
            $(tagname).html(data[0]);
        },
        error: function(data) {
            tagname = '#thumb_message' + id;
            $(tagname).html(' 이미 눌렀습니다.');
        }
    });
}

function burst_call_animation(count, finish, tagname, tagnamemsg) {
    var id = setInterval(frame, 100);
    function frame() {
        if (count == finish) {
            $(tagname).removeClass('magictime vanishIn');
            $(tagname).css('background-color', '#fff');
            $(tagnamemsg).html(' 버스터콜을 날렸습니다.');
            clearInterval(id);
        } else {
            count++;
            if (count % 2 == 0)
                $(tagname).css('background-color', '#fff');
            else {
                $(tagname).css('background-color', '#ff0');
            }
            $(tagname).html(count);
        }
    }
}

function pre_animation(count, finish, tagname, tagnamemsg) {
    var id = setInterval(frame, 100);
    timer_count = 0;
    $(tagname).addClass('magictime vanishIn');
    function frame() {
        if (timer_count == 10) {
            $(tagname).removeClass('magictime vanishIn');
            clearInterval(id);
            burst_call_animation(count, finish, tagname, tagnamemsg);
        } else {
            timer_count++;
        }
    }
}

function burst_call(id, nolook) {
    if (confirm("포인트를 모두 소진해 이 기사에 버스터 콜을 날리시겠습니까?")) {
        $.ajaxSetup({
            beforeSend: function(xhr, settings) {
                xhr.setRequestHeader("X-CSRFToken", $("input[name=csrfmiddlewaretoken]").val());
            }
        });
        $.ajax({
            type: "POST",
            url: "/api/burst_call/",
            data: {
                id: id,
                nolook: nolook
            },
            success: function(data) {
                tagname = '#thumb_up_msg' + id;
                if (nolook == 'nolook') {
                    tagname = '#thumb_down_msg' + id;
                }
                if (data[0] == 0) {
                    tagname = '#thumb_message' + id;
                    $(tagname).html(' 다음주에 다시 날려주세요.');
                }
                else {
                    count = $(tagname).html();
                    finish = data[0];
                    tagnamemsg = '#thumb_message' + id;
                    pre_animation(count, finish, tagname, tagnamemsg);
                }

            },
            error: function(data) {
                tagname = '#thumb_message' + id;
                $(tagname).html(' 포인트가 부족합니다.');
            }
        });
    }
}
