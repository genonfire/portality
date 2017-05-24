function claim(e) {
  var email = document.getElementById("email").value;
  var subject = document.getElementById("subject").value;
  var url = document.getElementById("url").value;

  if (!subject || !url) {
    var empty = "";
    if (!subject)
      empty += "기사 제목";
    if (!url)
      empty += ", 기사 주소";
    alert("다음 항목이 비어 있습니다. [" + empty + "]");
    return;
  }

  $.ajax({
    url: 'http://portal.gencode.me/api/call/',
    method: 'POST',
    crossDomain: false,
    dataType: 'json',
    data: {
      'email': email,
      'subject': subject,
      'url': url,
      'claimusers': ''
    },
    success: function(data) {
      $('#content').html(data['count'] + "번째 버스터 콜을 날렸습니다.");
    },
    error: function(XMLHttpRequest, textStatus, errorThrown) {
      $('#content').html(errorThrown);
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
