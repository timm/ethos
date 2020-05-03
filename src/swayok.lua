local the = require "the"
local oo  = the.oo
require "ok"

Data= require "data"
Sway = require "sway"

local function some1(  d,s)
  d=Data()
  d:read(the.csv .. 'auto93.csv')
  print("==========")
  s=Sway(d)
  s.debug = true
  d:clone( s:select())
end

some1()

ok{some = some1}
