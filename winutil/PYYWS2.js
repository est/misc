/* !
 * Ping Your Yesterdays's WinOMeter Statistics - PYYWS2.js
 * By est, electronicstar@126.com
 * Copyleft @ 2009
 */

//put your Ping.fm authentication key (https://ping.fm/key/) here
var AUTH = "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX-XXXXXXXXXX";


/* --------------------- WinOMeter part --------------------- */

var shell   = new ActiveXObject("WScript.Shell");
var history = shell.RegRead("HKEY_CURRENT_USER\\Software\\Tomas Jelinek\\WinOMeter\\History").toArray();
var dupcheck_key = "HKEY_CURRENT_USER\\Software\\Tomas Jelinek\\WinOMeter\\last_PYYWS2";

var item, d = new Date();
var s = [d.getDate()-1, d.getMonth()+1, d.getFullYear() % 256, Math.floor(d.getFullYear()/256)].toString();
for(var i=history.length-24; i>=0; i-=24)
{
    item = history.slice(i, i+24);
    if(item.slice(0, 4).toString() == s) break;
}

/* date         key p           mouse t         r       m       l               uptime
 * 0c,05,d9,07, dc,7b,00,00,    86,82,03,4a,    16,03,  8b,5b,  e5,46,00,00,    1a,b0,00,00, 
 * 12,5,217,7,  220,123,0,0,    134,130,3,74,   22,3,   139,91, 229,70,0,0,     26,176,0,0
 */

function rs(l)
{
    var c=0;
    for(var i=0;i<l.length;i++)
    {
        c += l[i] * Math.pow(256, i);
    }
    return c
}

// 32-bit IEEE 754 floating point from http://code.google.com/p/jspack/ by Fair Oaks Labs, Inc.
// example: decode_ieee754( [72, 176, 78, 28] ) get 361072.875
decode_ieee754 = function (a)
{
    var s, e, m, i, d, nBits, mLen, eLen, eBias, eMax;
    var el = {len:4, mLen:23, rt:Math.pow(2, -24)-Math.pow(2, -77)};
    var bBE = false; //big-endianness
    mLen = el.mLen, eLen = el.len*8-el.mLen-1, eMax = (1<<eLen)-1, eBias = eMax>>1;

    i = bBE?0:(el.len-1); d = bBE?1:-1; s = a[i]; i+=d; nBits = -7;
    for (e = s&((1<<(-nBits))-1), s>>=(-nBits), nBits += eLen; nBits > 0; e=e*256+a[i], i+=d, nBits-=8);
    for (m = e&((1<<(-nBits))-1), e>>=(-nBits), nBits += mLen; nBits > 0; m=m*256+a[i], i+=d, nBits-=8);

    switch (e)
    {
        case 0:
            // Zero, or denormalized number
            e = 1-eBias;
            break;
        case eMax:
            // NaN, or +/-Infinity
            return m?NaN:((s?-1:1)*Infinity);
        default:
            // Normalized number
            m = m + Math.pow(2, mLen);
            e = e - eBias;
            break;
    }
    return (s?-1:1) * m * Math.pow(2, e-mLen);
};


kp = rs(item.slice(4, 8));                      //key presses
mt = decode_ieee754(item.slice(8, 12))/1000;    //Mouse Trajectory
rc = rs(item.slice(12, 14));	                //right clicks	
mc = rs(item.slice(14, 16));	                //middle clicks	
lc = rs(item.slice(16, 20));	                //left clicks
ut = rs(item.slice(20, 24));	                //uptime in seconds
uth = Math.floor(ut / 3600)
utm = Math.floor( (ut-uth*3600)/60 )
uts = ut - uth*3600 - utm*60
ut = uth+'h'+utm+'m'+uts+'s'                    //uptime in 12h34m56s

//content to be sent to ping.fm/twitter
text = "WinOMeter yesterday for @est: key presses: "+kp+", mouse trajectory: "+mt+"m, L/M/R clicks: "+lc+"/"+mc+"/"+rc+", uptime: "+ut+" #PYYWS"



/* --------------------- ping.fm part --------------------- */
//WScript.Echo(0);

var xhr = new ActiveXObject("MsXml2.XmlHttp");
function post_to_pingfm(text)
{
    xhr.Open("POST", "http://api.ping.fm/v1/user.post", 0);
    xhr.setRequestHeader("Content-type", "application/x-www-form-urlencoded")
    xhr.Send("api_key=0b48e29f10e6f46acb1d9974f32be075&user_app_key=" + AUTH + "&post_method=default&body=" + encodeURIComponent(text))
    return xhr.getResponseBody
}

try
{
    posted = shell.RegRead(dupcheck_key);
}
catch(e)
{
    shell.RegWrite(dupcheck_key, "sth");
}

try
{
    if(shell.RegRead(dupcheck_key)!=s)
    {
        //WScript.Echo
        post_to_pingfm(text);
    }
    shell.RegWrite(dupcheck_key, s);
}
catch(e)
{
    WScript.Echo(e)
}
