let symbols = {
  'EUR': '€',
  'USD': '$',
  'GBP': '£',
}

export const codeToSymbol = (code) => (
  symbols[code]
)
