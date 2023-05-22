import { Controller } from "../../node_modules/@hotwired/stimulus"
import trumbowyg from '../../node_modules/trumbowyg';

$.trumbowyg.svgPath = '/static/node_modules/trumbowyg/dist/ui/icons.svg';

// Usage: connect directly on text-area element
export default class extends Controller {

  connect() {
    $(this.element).trumbowyg();
  }

}
