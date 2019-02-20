class Solution:
    def divide(self, dividend, divisor):
        """
        :type dividend: int
        :type divisor: int
        :rtype: int
        """
        if dividend == 0:
            return 0
        elif divisor==1：
            return dividend
        elif divisor==-1:
            return -dividend
        else:
            if abs(dividend) < abs(divisor):
                return 0
            
            else:
                i = 1
                abs_divisor = abs(divisor)
                while abs(dividend) >= pow(abs_divisor,i):
                    i += 1
                    if i > 31:
                        break
                    
                if i > pow(2,31):
                    return pow(2,31)-1
                else:
                    if (dividend>0) == (divisor>0):
                        return i-1
                    else:
                        return -(i-1)
                    
