import * as moment from 'moment'

export default {

  // Filtre permettant d'arrondir un nombre avec tant de décimales.
  round (value, decimal) {
    if (value === undefined) {
      return ''
    }
    let factor = Math.pow(10, decimal)
    return Math.round(value * factor) / factor
  },

  currencySymbol (value) {
    let symbols = {
      'EUR': '€',
      'USD': '$',
      'GBP': '£'
    }
    return symbols[value]
  },

  dateEnToFr (date) {
    return moment(date, 'YYYY/MM/DD').format('DD/MM/YYYY')
  }
}
