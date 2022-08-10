const path = require('path')
const publicIp = require('public-ip')
const internalIp = require('internal-ip')
const express = require('express')
const expressWs = require('express-ws')
const colours = require('colors/safe')
//const router = express.Router();

const CloudServer = require('./cloud-server.js')
const fsUtil = require('./util.js')

/*function cal_cookie(){
  rand_data = fetch("https://www.random.org/integers/?num=1024&min=1&max=100&format=plain&col=1&rnd=new&base=10").then(()=>{
    console.log(rand_data.Text)
  })
}
function get_user_id(){
  cal_cookie()
}
let uid_url = "../static/"+ "get_user_id.html"
console.log(uid_url)*/
console.log("CON*.LOG TEST")



async function startServer ({ port, lockVars, perMessageDeflate, python_port }) {
  const app = express()
  const cloudServer = new CloudServer({ lockVars })
  // the http stuff is handled by python because python can handle post requests without my brain exploding to get it working,
  // unlike express here, but we still need it for the ws connections so express gets to host an emtpy folder for http because python will do the real hosting.
  // python will gen api keys/user IDs and javascript will read those things from a file.
  // also because i can't figure out how to disable only http in express (you probably just can't) so python will be on port 8003

  app.set("views", __dirname+"../empty_express_http_dir")
  app.disable('x-powered-by')
//  app.disable('express')
  expressWs(app, undefined, {
    wsOptions: { perMessageDeflate }
  })
  // only for old installs of the main branch
/*  const oldIndexHtmlPath = path.resolve(__dirname, '../index.html')
  if (await fsUtil.exists(oldIndexHtmlPath)) {
    app.get('/', (req, res, next) => {
      res.sendFile(oldIndexHtmlPath)
    })
  }
  
  app.use(express.static(path.resolve(__dirname, '../static/'), {
    extensions: ['html', 'htm']
  }))*/


  app.ws('/', cloudServer.handleWsConnection)

/*  app.use((req, res) => {
    res.status(404).sendFile(path.resolve(__dirname, '../static/404.html'))
  })*/
  app.listen(port, async () => {
    console.log(colours.green('I\'m now running your cloud server!'))
    console.log('You can access it...')
    console.log(`  • on your computer at ${colours.cyan(`ws://localhost:${port}/`)} (use this for testing)`)
    const privateIp = await internalIp.v4().catch(() => null)
    if (privateIp) {
      console.log(`  • locally within your network at ${colours.blue(`ws://${privateIp}:${port}/`)} (maybe)`)
    }
    const ip = await publicIp.v4().catch(() => null)
    if (ip) {
      console.log(`  • publicly at ${colours.blue(`ws://${ip}:${port}/`)}, but ONLY if you've set up port forwarding on your router`)
    }
    console.log(colours.yellow(`python is also serving files from the static/ folder, which you can access in your browser at ${colours.blue(`http://localhost:${python_port}/`)}.`))
    console.log(colours.red('Press control+C to stop the server.'))
  })
}

module.exports = startServer
