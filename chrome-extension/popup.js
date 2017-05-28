function claim(e) {
  var email = document.getElementById("email").value;
  var subject = document.getElementById("subject").value;
  var url = document.getElementById("url").value;
  var nolook = $('input[name=nolook]:checked').val() == 'true' ? true : false

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
    url: 'http://nolooknews.com/api/call/',
    method: 'POST',
    crossDomain: false,
    dataType: 'json',
    data: {
      'email': email,
      'subject': subject,
      'url': url,
      'nolook': nolook,
      'claimusers': ''
    },
    success: function(data) {
      if (nolook)
        msg = '나빠요!'
      else
        msg = '좋아요!'
      $('#content').html(data + "번째 " + msg + "를 날렸습니다.");
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
