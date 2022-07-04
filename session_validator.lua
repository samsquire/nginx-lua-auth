local io = require "ngx.io"

local session_cookie = ngx.var.cookie_session
if session_cookie == nil then
	
	ngx.log(ngx.STDERR, 'Session cookie was nil')
	ngx.exec("/auth")	
	return
end
ngx.log(ngx.STDERR, 'Validating user cookie')
ngx.log(ngx.STDERR, 'Session cookie is ' .. session_cookie)
local safe_cookie = string.gsub(session_cookie, "[^a-zA-Z0-9]+", "") 

local f = io.open("/etc/nginx/sessions/" .. safe_cookie, "r")
if f == nil then 
		
	ngx.log(ngx.STDERR, 'NIL COOKIE Session cookie is ' .. safe_cookie)
	ngx.exec("/auth")	
	return true 
else 
	valid_ip_address = f:read("*a")
	if not valid_ip_address == ngx.var.remote_addr then
		ngx.exec("/auth")	
	end
	f:close() 
	return false 
end

