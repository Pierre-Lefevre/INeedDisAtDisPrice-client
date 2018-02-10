let serverPort = 4242
let serverHost = 'localhost'
// let serverHost = '90.29.160.210'

module.exports = {
  serverPort,
  serverHost,
  serverUrl: 'http://' + serverHost + ':' + serverPort
}
