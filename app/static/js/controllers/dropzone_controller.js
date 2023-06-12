import { Controller } from "../../node_modules/@hotwired/stimulus"
import Dropzone from "../../node_modules/dropzone"
import dropzone from "../../node_modules/dropzone"

export default class extends Controller {
    static targets = ["dropzone"]

    connect() {
        Dropzone.options.dropzone = {
            // Note: using "function()" here to bind `this` to
            // the Dropzone instance.
            init: function() {
                this.on("queuecomplete", file => {
                    location.reload();
                });
            }
        };

        $(this.element).dropzone({
            url: this.element.action,
            acceptedFiles: ".pdf, .png, .jpg, .jpeg, .gif"
        });
    }

}
