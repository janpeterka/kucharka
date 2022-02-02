Stimulus.register("scroller", class extends Controller {
  static get targets() {
    return ["scroller"]
  }

  connect() {
    this.scrollerTarget.innerHTML = this._down_symbol() + this._up_symbol()
  }

  scrollToBottom(event) {
    window.scrollTo(0,document.body.scrollHeight);
  }

  scrollToTop(event) {
    window.scrollTo(0,0);
  }

  _down_symbol(){
    return '\
    <i class="fas fa-chevron-circle-down" \
       style="position: fixed; bottom:2rem; right:2rem; font-size:3rem; opacity: 0.5; z-index:100;" \
       data-action="click->scroller#scrollToBottom"> \
    </i>'
  }

  _up_symbol(){
    return '\
    <i class="fas fa-chevron-circle-up" \
       style="position: fixed; bottom:6rem; right:2rem; font-size:3rem; opacity: 0.5; z-index:100;" \
       data-action="click->scroller#scrollToTop"> \
    </i>'
  }

})
