Stimulus.register("clipboard", class extends Controller {
    static get targets() {
      return ["source"]
    }

  connect() {
  }

  copy() {
    // this.sourceTarget.select()
    // document.execCommand("copy")
    let text = this.sourceTarget.value

    if (text==undefined) {
      text = this.sourceTarget.innerHTML
    }

    this._copyTextToClipboard(text);

  }

  _fallbackCopyTextToClipboard(text) {
    var textArea = document.createElement("textarea");
    textArea.value = text;
    
    // Avoid scrolling to bottom
    textArea.style.top = "0";
    textArea.style.left = "0";
    textArea.style.position = "fixed";

    document.body.appendChild(textArea);
    textArea.focus();
    textArea.select();

    try {
      var successful = document.execCommand('copy');
      var msg = successful ? 'successful' : 'unsuccessful';
      console.log('Fallback: Copying text command was ' + msg);
    } catch (err) {
      console.error('Fallback: Oops, unable to copy', err);
    }

    document.body.removeChild(textArea);
  }

  _copyTextToClipboard(text) {
    if (!navigator.clipboard) {
      this._fallbackCopyTextToClipboard(text);
      return;
    }
    navigator.clipboard.writeText(text).then(function() {
      console.log('Async: Copying to clipboard was successful!');
    }, function(err) {
      console.error('Async: Could not copy text: ', err);
    });
  }

})
