Stimulus.register("set-default-dates", class extends Controller {
    static get targets() {
      return ["dateFrom", "dateTo"]
    }

  connect() {
    var today = new Date();

    this.dateFromTarget.valueAsDate = today;
    this.dateToTarget.valueAsDate = this._addDays(today, 14);
  }

  _addDays(date, days) {
    var result = new Date(date);
    result.setDate(result.getDate() + days);
    return result;
  }
})
