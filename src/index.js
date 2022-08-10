const parseArgs = require('minimist')

const startServer = require('./server.js')

const {
  port = 8002,
  lock,
  'per-message-deflate': perMessageDeflate,
  help,
  python_port = "NOT SET, THE WEBSERVER IS NOT RUNNING"
} = parseArgs(process.argv.slice(2), {
  boolean: ['lock', 'per-message-deflate', 'help'],
  alias: {
    p: 'port',
    l: 'lock',
    D: 'per-message-deflate',
    h: 'help',
    pyport: 'pyp'
  }
})

if (help) {
  console.log('npm start -- [OPTIONS]')
  console.log('--port=<port> (-p <port>)\n\tSet the port for the server. (Default 8002 for j0\'s cloud server)')
  console.log('--lock (-l)\n\tDisables the ability to rename and delete cloud variables. (Enabled by default)')
  console.log('--per-message-deflate (-D)\n\tEnable permessage-deflate compression, which has a slight impact on performance (Disabled by default)')
  console.log('--help (-h)\n\tDisplay help')
  console.log('--python_port=<python webserver port>\n\tthis is set by python when starting the javascript server.\n\tall this does is tell what the server to say the webserver port is.')
  process.exit(0)
} else {
  startServer({ port, lockVars: lock, perMessageDeflate,python_port })
}
