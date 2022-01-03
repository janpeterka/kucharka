Stimulus.register("set-duration", class extends Controller {
    static get targets() {
      return ["dateFrom", "dateTo", "duration"]
    }

  connect() {
    this.update_duration()
  }

  update_duration() {
    var duration = this._duration()
    var days_text = ""
    if (duration == 1) {
      days_text = "den"
    } else if (duration > 1 && duration <= 4 ) {
      days_text = "dny"
    } else {
      days_text = "dnů"
    }

    this.durationTarget.value = duration + " " + days_text
  }

  _duration(startDate, endDate) {
    var millisecondsPerDay = 24 * 60 * 60 * 1000;
    var startDate = this.dateFromTarget.valueAsDate
    var endDate = this.dateToTarget.valueAsDate

    return (this._treatAsUTC(endDate) - this._treatAsUTC(startDate)) / millisecondsPerDay;
  }

  _treatAsUTC(date) {
    var result = new Date(date);
    result.setMinutes(result.getMinutes() - result.getTimezoneOffset());
    return result;
  }

})
