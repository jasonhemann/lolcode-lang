b=.596 pi2=3.142/2 u=57.295 k=100 o=192
x=(:r1*k)/o :angle1=(b*x+x*x)/(1+(2*b*x)+x*x)*u*pi2 goto 2

// Store angle to a target as :angle1
//  o = horizontal offset