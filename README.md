# nginx-lua-auth

You can create an incredibly scalable hybrid static website by using Lua with Nginx. This uses the [lua-io-nginx-module module](https://github.com/tokers/lua-io-nginx-module#fileread)

Users can be logged in but still reach 13,000 requests per second this is due to the website being partially static.

The first benchmark shows an authenticated user accessing the static site with a cookie. The second shows an unauthenticated user, hitting the proxy.

```
sam@sam-devbox:~/wrk$ ./wrk -t12 -c400 -d30s http://127.0.0.1:8080/ -H "Cookie: session=bb2e055e10f54d6f9f1272fbbf562f23"
Running 30s test @ http://127.0.0.1:8080/
  12 threads and 400 connections
  Thread Stats   Avg      Stdev     Max   +/- Stdev
    Latency    33.00ms   41.28ms   1.23s    99.22%
    Req/Sec     1.10k   177.20     2.05k    72.33%
  391843 requests in 30.07s, 97.16MB read
Requests/sec:  13031.63
Transfer/sec:      3.23MB
sam@sam-devbox:~/wrk$ ./wrk -t12 -c400 -d30s http://127.0.0.1:8080/
Running 30s test @ http://127.0.0.1:8080/
  12 threads and 400 connections
  Thread Stats   Avg      Stdev     Max   +/- Stdev
    Latency   339.87ms   24.39ms 409.90ms   93.84%
    Req/Sec    99.61     76.39   343.00     68.71%
  30998 requests in 30.10s, 11.80MB read
  Socket errors: connect 0, read 507753, write 0, timeout 0
Requests/sec:   1029.98
Transfer/sec:    401.33KB
```

Please see [my Medium article 3288 requests while logged in](https://medium.com/@samuelmichaelsquire/1633-requests-a-second-while-logged-in-3bca95cf3cf1) for an alternative approach to this problem that uses a Rust Redis session authenticator.

# Installation

Building Nginx with Lua 

```
export LUAJIT_INC=/usr/local/include/luajit-2.1/
export LUAJIT_LIB=/usr/local/lib/
git clone git@github.com:openresty/luajit2.git
git clone git@github.com:openresty/lua-resty-lrucache.git
git clone git@github.com:openresty/lua-resty-core.git
git clone git@github.com:sto/ngx_http_auth_pam_module.git
git clone git@github.com:samsquire/nginx-lua-auth.git
git clone git@github.com:tokers/lua-io-nginx-module.git
git clone git@github.com:openresty/lua-nginx-module.git
git clone git@github.com:vision5/ngx_devel_kit.git
# PCRE2-10.38 tarball from git releases github.com/PCRE/pcre2.git

./configure --prefix=/opt/nginx          --with-ld-opt="-Wl,-rpath,/usr/local/lib/ -lpcre"          --add-module=/home/sam/ngx_devel_kit          --add-module=/home/sam/lua-nginx-module  --with-threads --add-module=/home/sam/lua-io-nginx-module --with-pcre=/home/sam/Downloads/pcre2-10.38 --add-module=/home/sam/ngx_http_auth_pam_module
```

Follow [these openresty Lua instructions](https://github.com/openresty/lua-nginx-module/).

Copied the instructions as a backup.

I uses the latest nginx sourcecode. 

```
nginx version: nginx/1.23.0
built by gcc 11.2.0 (Ubuntu 11.2.0-19ubuntu1) 
configure arguments: --prefix=/opt/nginx --with-ld-opt='-Wl,-rpath,/usr/local/lib/ -lpcre' --add-module=/home/sam/ngx_devel_kit --add-module=/home/sam/lua-nginx-module --with-threads --add-module=/home/sam/lua-io-nginx-module --with-pcre=/home/sam/Downloads/pcre2-10.38 --add-module=/home/sam/ngx_http_auth_pam_module

```

```
 wget 'https://openresty.org/download/nginx-1.19.3.tar.gz'
 tar -xzvf nginx-1.19.3.tar.gz
 cd nginx-1.19.3/

 # tell nginx's build system where to find LuaJIT 2.0:
 export LUAJIT_LIB=/path/to/luajit/lib
 export LUAJIT_INC=/path/to/luajit/include/luajit-2.0

 # tell nginx's build system where to find LuaJIT 2.1:
 export LUAJIT_LIB=/path/to/luajit/lib
 export LUAJIT_INC=/path/to/luajit/include/luajit-2.1

 # Here we assume Nginx is to be installed under /opt/nginx/.
 ./configure --prefix=/opt/nginx \
         --with-ld-opt="-Wl,-rpath,/path/to/luajit/lib" \
         --add-module=/path/to/ngx_devel_kit \
         --add-module=/path/to/lua-nginx-module

 # Note that you may also want to add `./configure` options which are used in your
 # current nginx build.
 # You can get usually those options using command nginx -V

 # you can change the parallelism number 2 below to fit the number of spare CPU cores in your
 # machine.
 make -j2
 make install

 # Note that this version of lug-nginx-module not allow to set `lua_load_resty_core off;` any more.
 # So, you have to install `lua-resty-core` and `lua-resty-lrucache` manually as below.

 cd lua-resty-core
 make install PREFIX=/opt/nginx
 cd lua-resty-lrucache
 make install PREFIX=/opt/nginx

 # add necessary `lua_package_path` directive to `nginx.conf`, in the http context
```

WARNING: To get lua-resty-core and lua-resty-lrucache to install, I had to move the files the make install of them did into /usr/local/share/lua/5.1/resty. The make install installs the files into the wrong directory that nginx doesn't look at.

Install. Install gunicorn.

```
sudo bash install.sh
sudo /opt/nginx/sbin/nginx -c /etc/nginx/nginx.conf
sudo bash start.sh
```

Go to http://localhost:8080/
Login with user sam sam
