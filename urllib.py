#使用Python访问网页主要有三种方式： urllib, urllib2, httplib.urllib比较简单，功能相对也比较弱，httplib简单强大，但好像不支持session

urllib2


1. 最简单的页面访问

res=urllib2.urlopen(url)

print res.read().decode('utf-8', 'ignore')


2. 加上要get或post的数据
data={"name":"hank", "passwd":"hjz"}

urllib2.urlopen(url, urllib.urlencode(data))


3. 加上http头

header={"User-Agent": "Mozilla-Firefox5.0"}
urllib2.urlopen(url, urllib.urlencode(data), header)

使用opener和handler
opener = urllib2.build_opener(handler)

urllib2.install_opener(opener)


4. 加上session

cj = cookielib.CookieJar() #在内存中加载cookie

cookie = cookielib.LWPCookieJar() #在硬盘中存储cookie

cjhandler=urllib2.HTTPCookieProcessor(cj)
opener = urllib2.build_opener(cjhandler)

urllib2.install_opener(opener)



5. 加上 Basic 认证
当需要Authentication的时候，服务器发送一个头（同时还有401代码）请求Authentication。它详细指明了一个Authentication和一个域。这个头看起来像：

Www-authenticate: SCHEME realm=”REALM”.
e.g.
Www-authenticate: Basic realm=”cPanel Users”

客户端然后就会用包含在头中的正确的帐户和密码重新请求这个域。这是”基本验证”。为了简化这个过程，我们可以创建一个 HTTPBasicAuthHandler和opener的实例来使用这个handler。
HTTPBasicAuthHandler用一个叫做密码管理的对象来处理url和用户名和密码的域的映射。如果你知道域是什么（从服务器发送的authentication
头中），那你就可以使用一个HTTPPasswordMgr。多数情况下人们不在乎域是什么。那样使用HTTPPasswordMgrWithDefaultRealm就很方便。它
允许你为一个url具体指定用户名和密码。这将会在你没有为一个特殊的域提供一个可供选择的密码锁时提供给你。我们通过提供None作为add_password方法域的参数指出这一点。
最高级别的url是需要authentication的第一个url。比你传递给.add_password()的url更深的url同样也会匹配。

password_mgr = urllib2.HTTPPasswordMgrWithDefaultRealm() # create a password manager
top_level_url = "http://www.163.com/"
password_mgr.add_password(None, top_level_url, username, password)
handler = urllib2.HTTPBasicAuthHandler(password_mgr)
opener = urllib2.build_opener(handler)  #creater 'opener'(OpenerDirector instance)

urllib2.install_opener(opener) #install the opener



6. 使用代理
# opener = urllib2.OpenerDirector()
# proxy_support = urllib2.ProxyHandler({'http': 'http://1.2.3.4:3128/'})
# opener.add_handler(proxy_support)
# urllib2.install_opener(opener)

proxy_support = urllib2.ProxyHandler({"http":"http://1.2.3.4:3128/"})
opener = urllib2.build_opener(proxy_support)
f = opener.open('http://www.baidu.com/')

urllib2.install_opener(opener)

7.FTP

import urllib2

handler = urllib2.FTPHandler()
request = urllib2.Request(url='ftp://用户名:密码@ftp地址/')
opener = urllib2.build_opener(handler)
f = opener.open(request)
print f.read()


8. 设置超时

socket.setdefaulttimeout(5)


1 Proxy 的设置


urllib2 默认会使用环境变量 http_proxy 来设置 HTTP Proxy。如果想在程序中明确控制 Proxy，而不受环境变量的影响，可以使用下面的方式


importurllib2  

enable_proxy = True 

proxy_handler = urllib2.ProxyHandler({"http": 'http://some-proxy.com:8080'}) 

null_proxy_handler =urllib2.ProxyHandler({})  

if enable_proxy: 

    opener =urllib2.build_opener(proxy_handler) 

else: 

    opener = urllib2.build_opener(null_proxy_handler)  urllib2.install_opener(opener) 


这里要注意的一个细节，使用 urllib2.install_opener() 会设置 urllib2 的全局 opener。这样后面的使用会很方便，但不能做更细粒度的控制，比如想在程序中使用两个不同的 Proxy 设置等。比较好的做法是不使用 install_opener 去更改全局的设置，而只是直接调用 opener 的 open 方法代替全局的 urlopen 方法。

2 Timeout 设置

在老版本中，urllib2 的 API 并没有暴露 Timeout 的设置，要设置 Timeout 值，只能更改 Socket 的全局 Timeout 值。

importurllib2 

importsocket  

socket.setdefaulttimeout(10) # 10 秒钟后超时 

urllib2.socket.setdefaulttimeout(10) # 另一种方式 

在新的 Python 2.6 版本中，超时可以通过 urllib2.urlopen() 的 timeout 参数直接设置。

import urllib2 

response = urllib2.urlopen('http://www.google.com', timeout=10) 


3 在 HTTP Request 中加入特定的 Header

要加入 Header，需要使用 Request 对象：


import urllib2 


request = urllib2.Request(uri) 

request.add_header('User-Agent', 'fake-client') 

response = urllib2.urlopen(request) 


对有些 header 要特别留意，Server 端会针对这些 header 做检查
•User-Agent 有些 Server 或 Proxy 会检查该值，用来判断是否是浏览器发起的 Request
•Content-Type 在使用 REST 接口时，Server 会检查该值，用来确定 HTTP Body 中的内容该怎样解析。 

常见的取值有：
•application/xml ：在 XML RPC，如 RESTful/SOAP 调用时使用
•application/json ：在 JSON RPC 调用时使用
• 
application/x-www-form-urlencoded ：浏览器提交 Web 表单时使用

•…… 

在使用 RPC 调用 Server 提供的 RESTful 或 SOAP 服务时， Content-Type 设置错误会导致 Server 拒绝服务。



4 Redirect

urllib2 默认情况下会针对 3xx HTTP 返回码自动进行 Redirect 动作，无需人工配置。要检测是否发生了 Redirect 动作，只要检查一下 Response 的 URL 和 Request 的 URL 是否一致就可以了。

 
importurllib2 


response =urllib2.urlopen('http://www.google.cn') 

whether_redirected = response.geturl() == 'http://www.google.cn' 


如果不想自动 Redirect，除了使用更低层次的 httplib 库之外，还可以使用自定义的 HTTPRedirectHandler 类。

 
import urllib2  


class RedirectHandler(urllib2.HTTPRedirectHandler): 

    def http_error_301(self, req, fp, code, msg, headers): 

        pass     

    def http_error_302(self, req, fp, code, msg, headers): 

        pass  

opener =urllib2.build_opener(RedirectHandler) 

opener.open('http://www.google.cn') 


5 Cookie


urllib2 对 Cookie 的处理也是自动的。如果需要得到某个 Cookie 项的值，可以这么做：

import urllib2 

import cookielib  


cookie =cookielib.CookieJar() 

opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookie)) 
response = opener.open('http://www.google.com') 

for item in cookie: 

    if item.name == 'some_cookie_item_name': 

        print item.value 


6 使用 HTTP 的 PUT 和 DELETE 方法


urllib2 只支持 HTTP 的 GET 和 POST 方法，如果要使用 HTTP PUT 和 DELETE，只能使用比较低层的 httplib 库。虽然如此，我们还是能通过下面的方式，使 urllib2 能够发出 HTTP PUT 或 DELETE 的包：

importurllib2  

request =urllib2.Request(uri, data=data) 

request.get_method = lambda: 'PUT'# or 'DELETE' 

response = urllib2.urlopen(request) 


这种做法虽然属于 Hack 的方式，但实际使用起来也没什么问题。


7 得到 HTTP 的返回码


对于 200 OK 来说，只要使用 urlopen 返回的 response 对象的 getcode() 方法就可以得到 HTTP 的返回码。但对其它返回码来说，urlopen 会抛出异常。这时候，就要检查异常对象的 code 属性了：


importurllib2 

try: 

    response =urllib2.urlopen('http://restrict.web.com') 

except urllib2.HTTPError, e: 

    print e.code 


8 Debug Log


使用 urllib2 时，可以通过下面的方法把 Debug Log 打开，这样收发包的内容就会在屏幕上打印出来，方便我们调试，在一定程度上可以省去抓包的工作。


import urllib2 


httpHandler =urllib2.HTTPHandler(debuglevel=1) 

httpsHandler =urllib2.HTTPSHandler(debuglevel=1) 

opener =urllib2.build_opener(httpHandler, httpsHandler)  urllib2.install_opener(opener) 

response = urllib2.urlopen('http://www.google.com') 



