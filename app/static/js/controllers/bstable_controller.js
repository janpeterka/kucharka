import { Controller } from "../../node_modules/@hotwired/stimulus"

export default class extends Controller {
    connect(){
        // This makes pages with table not use cache, which makes table load as it should on restoration (back navigation) visits.
        // However, it obviously makes these visits slower.
        Turbo.cache.exemptPageFromCache()
        $(this.element).bootstrapTable()
    }
}
