local the = require "the"
local oo  = the.oo
require "ok"

Data= require "data"
Div = require "div"

local function some1(  d)
  d=Data()
  d:read(the.csv .. 'auto93.csv')
  Div(d)
end

some1()

ok{some = some1}
