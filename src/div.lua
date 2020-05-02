local the = require "the"
local lib = require "lib"
local Div = the.class()

function Div:_init(data,   rows,cols,min,far,n)
  self.data = data
  self.rows = rows or data.rows
  self.cols = cols or data.some.y
  self.min  = min  or the.fmap.min 
  print(33)
  self.min  = (#self.rows)^self.min
  self.far  = far  or the.fmap.far
  self.n    = n    or the.fmap.n
  self.some = lib.anys( self.rows, self.n )
end

function Div:go()
  if #self.rows > 2*self.min then
    Div(self.data, self:split(), self.cols, self.min, 
        self.far,  self.n):go()
  else 
    for _,row in pairs(self.rows) do 
      row.best = true end end
end

function Div:split(    tmp,left,right,c,x,lo,hi,what)
  tmp   = lib.any(self.some)
  left  = self:distant(tmp)
  right = self:distant(left)
  c     = self:dist(left,right)
  x     = self:project(left,right,c)
  lo,hi = {},{}
  for _,row in pairs(self.rows) do
    what = row.tmpx <= x and lo or hi 
    what[#what+1] = row
  end
  return left:dominates(right, self.cols) and lo or ho
end 

function Div:project(left,right,c,     a,b,x)
  for _,row in pairs(self.rows) do
    a     = self:dist(row,left)
    b     = self:dist(row,right)
    x     = (a^2 + c^2 - b^2) / (2*c)
    row.x = math.max(0, math.min(1, x))
  end
  self.rows = lib.sort(rows, "x")
  return self.rows[ #self.rows //2 ].x
end

function Div:distant(row) 
  return self.data:distant(row,self.cols,self.some,self.far)
end

function Div:dist(row1,row2) 
  return self.data:dist(row1, row2, self.cols)
end

return Div
