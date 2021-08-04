<h1 align="center">NWSS</h1>
<h2 align="center">

  a very fast easy ligth, and vanilla python3 web server
  
</h2>
<h5 align="center">
  New Web Secure Server
  
</h5>


<h2 align="center">

[![Mentioned in Awesome Vue.js](https://awesome.re/mentioned-badge.svg)](https://github.com/ExCLoudVision)

</h2>

<p align="center">

<img src="https://img.shields.io/static/v1?label=made%20with&message=the%20%3C3&color=critical" >
  
<img src="https://img.shields.io/static/v1?label=python&message=100&color=blue">
</p>
<p align="center">
<img src="https://media.discordapp.net/attachments/862807476277346356/869354366140842024/nwss_logo.png?width=597&height=597">
</p>

## Project setup

```bash
git clone https://github.com/ExCLoudVision/nwss  
```

## Simple Example

```py
import nwss
serv = nwss.Server(80)
def example(*args):
  return "Hellow World"
serv.AddPath("/example", example)
serv.run()
```
