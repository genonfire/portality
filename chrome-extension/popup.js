function claim(e) {
  var email = document.getElementById("email").value;
  var subject = document.getElementById("subject").value;
  var url = document.getElementById("url").value;
  email = "honeybee@yna.co.kr"
  // subject = "[이슈플러스] 재벌 '저격수'에서 '저승사자'로 돌아온 김상조"

  if (!email || !subject || !url) {
    var empty = "";
    if (!email)
      empty += "이메일";
    if (!subject)
      empty += ", 기사 제목";
    if (!url)
      empty += ", 기사 주소";
    alert("다음 항목이 비어 있습니다. [" + empty + "]");
    return;
  }

  $.ajax({
    url: 'http://localhost:8000/api/issue/',
    method: 'POST',
    crossDomain: false,
    dataType: 'json',
    data: {
      'email': email,
      'subject': subject,
      'url': url
    },
    success: function(data) {
      console.log(data);
    },
    error: function(XMLHttpRequest, textStatus, errorThrown) {
      // alert(errorThrown);
      callback();
    }
  });
}

function onLoad() {
  chrome.tabs.query({
    active: true,
    lastFocusedWindow: true
  }, function(tabs) {
    var tab = tabs[0];
    document.getElementById("url").value = tab.url;
    chrome.tabs.executeScript( {
      code: "window.getSelection().toString();"
    }, function(selection) {
      document.getElementById("subject").value = selection[0];
    });
  });
  document.getElementById("email").focus();
}

window.addEventListener("load", function()
{
  document.getElementById("claim").addEventListener("click", claim);
}, true);

window.onload = onLoad;
