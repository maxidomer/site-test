const popWin = window.open('pop.html','popup window','menubar=true')
function setCookie(key, value, days) {
  const d = new Date()
  d.setTime( d.getTime() + ( days * 86400000 ))
  document.cookie = key + '=' + encodeURI(value) + '; expires =' + d.toUTCString() + ';'
}
function getCookie( key ) {
  if (document.cookie) {
    const pairs = decodeURI( document.cookie ).split(';')
    let i,name,value
    for(i = 0; i < pairs.length ; i++ ){
      name = (pairs[ i ].split('=')[ 0 ]).trim()
      if (name === key) {
        value = pairs[i].split('=')[ 1 ]
      }
    }
    return value
  }
}


setCookie('user','miker mcmcm,12345', 7)

const list = document.getElementById('lister')
let i,value = getCookie('user')
if (value.indexOf(',')) {
  value = value.split(',')
}
for (i = 0; i < value.length; i++) {
  lister.innerHTML += '<li>' + value[i]
}
