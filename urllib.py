使用Python访问网页主要有三种方式： urllib, urllib2, httplib.urllib比较简单，功能相对也比较弱，httplib简单强大，但好像不支持session


1. 最简单的页面访问

res=urllib2.urlopen(url)

print res.read()


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



5. 加上Basic认证
password_mgr = urllib2.HTTPPasswordMgrWithDefaultRealm()
top_level_url = "http://www.163.com/"
password_mgr.add_password(None, top_level_url, username, password)
handler = urllib2.HTTPBasicAuthHandler(password_mgr)
opener = urllib2.build_opener(handler)

urllib2.install_opener(opener)



6. 使用代理
proxy_support = urllib2.ProxyHandler({"http":"http://1.2.3.4:3128/"})
opener = urllib2.build_opener(proxy_support)

urllib2.install_opener(opener)



7. 设置超时

socket.setdefaulttimeout(5)






1 Proxy 的设置


urllib2 默认会使用环境变量 http_proxy 来设置 HTTP Proxy。如果想在程序中明确控制 Proxy，而不受环境变量的影响，可以使用下面的方式





1 
importurllib2  



2 
enable_proxy = True 



3 
proxy_handler = urllib2.ProxyHandler({"http": 'http://some-proxy.com:8080'}) 



4 
null_proxy_handler =urllib2.ProxyHandler({})  



5 
if enable_proxy: 



6 
    opener =urllib2.build_opener(proxy_handler) 



7 
else: 



8 
    opener = urllib2.build_opener(null_proxy_handler)  urllib2.install_opener(opener) 




  
这里要注意的一个细节，使用 urllib2.install_opener() 会设置 urllib2 的全局 opener。这样后面的使用会很方便，但不能做更细粒度的控制，比如想在程序中使用两个不同的 Proxy 设置等。比较好的做法是不使用 install_opener 去更改全局的设置，而只是直接调用 opener 的 open 方法代替全局的 urlopen 方法。

2 Timeout 设置


在老版本中，urllib2 的 API 并没有暴露 Timeout 的设置，要设置 Timeout 值，只能更改 Socket 的全局 Timeout 值。





1 
importurllib2 



2 
importsocket  



3 
  



4 
socket.setdefaulttimeout(10) # 10 秒钟后超时 



5 
urllib2.socket.setdefaulttimeout(10) # 另一种方式 

在新的 Python 2.6 版本中，超时可以通过 urllib2.urlopen() 的 timeout 参数直接设置。





1 
importurllib2 



2 
response = urllib2.urlopen('http://www.google.com', timeout=10) 







3 在 HTTP Request 中加入特定的 Header


要加入 Header，需要使用 Request 对象：





1 
importurllib2 



2 
   



3 
request =urllib2.Request(uri) 



4 
request.add_header('User-Agent', 'fake-client') 



5 
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

 





1 
importurllib2 



2 
  



3 
response =urllib2.urlopen('http://www.google.cn') 



4 
whether_redirected = response.geturl() == 'http://www.google.cn' 






如果不想自动 Redirect，除了使用更低层次的 httplib 库之外，还可以使用自定义的 HTTPRedirectHandler 类。

 





01 
importurllib2  



02 
  



03 
class RedirectHandler(urllib2.HTTPRedirectHandler): 



04 
    def http_error_301(self, req, fp, code, msg, headers): 



05 
        pass     



06 
    def http_error_302(self, req, fp, code, msg, headers): 



07 
        pass  



08 
  



09 
opener =urllib2.build_opener(RedirectHandler) 



10 
opener.open('http://www.google.cn') 







5 Cookie


urllib2 对 Cookie 的处理也是自动的。如果需要得到某个 Cookie 项的值，可以这么做：





1 
importurllib2 



2 
importcookielib  



3 
  



4 
cookie =cookielib.CookieJar() 



5 
opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookie)) response =opener.open('http://www.google.com') 



6 
for item in cookie: 



7 
    if item.name == 'some_cookie_item_name': 



8 
        print item.value 



 


6 使用 HTTP 的 PUT 和 DELETE 方法


urllib2 只支持 HTTP 的 GET 和 POST 方法，如果要使用 HTTP PUT 和 DELETE，只能使用比较低层的 httplib 库。虽然如此，我们还是能通过下面的方式，使 urllib2 能够发出 HTTP PUT 或 DELETE 的包：





1 
importurllib2  



2 
  



3 
request =urllib2.Request(uri, data=data) 



4 
request.get_method = lambda: 'PUT'# or 'DELETE' 



5 
response = urllib2.urlopen(request) 






这种做法虽然属于 Hack 的方式，但实际使用起来也没什么问题。


7 得到 HTTP 的返回码


对于 200 OK 来说，只要使用 urlopen 返回的 response 对象的 getcode() 方法就可以得到 HTTP 的返回码。但对其它返回码来说，urlopen 会抛出异常。这时候，就要检查异常对象的 code 属性了：





1 
importurllib2 



2 
try: 



3 
    response =urllib2.urlopen('http://restrict.web.com') 



4 
except urllib2.HTTPError, e: 



5 
    print e.code 







8 Debug Log


使用 urllib2 时，可以通过下面的方法把 Debug Log 打开，这样收发包的内容就会在屏幕上打印出来，方便我们调试，在一定程度上可以省去抓包的工作。





1 
import urllib2 



2 
    



3 
httpHandler =urllib2.HTTPHandler(debuglevel=1) 



4 
httpsHandler =urllib2.HTTPSHandler(debuglevel=1) 



5 
opener =urllib2.build_opener(httpHandler, httpsHandler)  urllib2.install_opener(opener) 



6 
response = urllib2.urlopen('http://www.google.com') 



