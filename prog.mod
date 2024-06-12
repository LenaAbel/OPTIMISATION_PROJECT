param T1, integer, >= 0;
param T2, integer, >= 0;
param T3, integer, >= 0;
param T4, integer, >= 0;

var tu1, >= 0;
var tu2, >= 0;
var tu3, >= 0;
var tu4, >= 0;

maximize obj: tu1 + tu2 + tu3 + tu4;

s.t. constraint1: tu2 + tu3 + tu4 <= T1;
s.t. constraint2: tu1 + tu2 <= T2;
s.t. constraint3: tu3 <= T3;
s.t. constraint4: tu1 + tu4 <= T4;

data;

param T1 := 6;
param T2 := 3;
param T3 := 2;
param T4 := 6;

end;
