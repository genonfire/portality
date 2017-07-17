function checkDuplication() {
    id_username = $('#id_username').val();
    if (!id_username) {
        alert("아이디를 입력하세요.");
        return;
    }
    $.ajaxSetup({
        crossDomain: false,
        beforeSend: function(xhr, settings) {
            xhr.setRequestHeader("X-CSRFToken", $("input[name=csrfmiddlewaretoken]").val());
        }
    });
    $.ajax({
        type: "POST",
        url: "/accounts/checkduplication/",
        data: {
            username: id_username
        },
        success: function(data) {
            alert(data.msg);
        },
        error: function(request, status, error) {
            alert("error: " + status);
        }
    });
}

function checkEmail() {
    id_email = $('#id_email').val();
    if (!id_email) {
        alert("이메일 주소를 입력하세요.");
        return;
    }
    else if (id_email.indexOf('@') < 1) {
        alert("올바른 이메일 주소를 입력하세요.")
        return;
    }
    $.ajaxSetup({
        crossDomain: false,
        beforeSend: function(xhr, settings) {
            xhr.setRequestHeader("X-CSRFToken", $("input[name=csrfmiddlewaretoken]").val());
        }
    });
    $.ajax({
        type: "POST",
        url: "/accounts/checkemail/",
        data: {
            email: id_email
        },
        success: function(data) {
            alert(data.msg);
        },
        error: function(request, status, error) {
            alert("이메일 발송에 실패했습니다. 나중에 다시 시도하세요.");
        }
    });
}

$('#signup_form').submit(function(e) {
    id_username = $('#id_username').val();
    id_email = $('#id_email').val();
    id_code = $('#id_code').val();
    id_password1 = $('#id_password1').val();
    id_password2 = $('#id_password2').val();
    concent = $('#concent').is(':checked')
    if (!concent) {
        e.preventDefault();
        alert("개인정보 취급방침에 동의해주세요.");
        return;
    }
    if (!id_username || !id_email || !id_password1 || !id_password2 || !id_code) {
        e.preventDefault();
        alert("비어있는 항목을 입력하세요.");
        return;
    }
    if (id_password1 != id_password2) {
        e.preventDefault();
        alert("비밀번호가 서로 다릅니다.");
        return;
    }
});
