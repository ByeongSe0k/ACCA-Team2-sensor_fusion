import numpy as np
import math

def isClose(x, y, rtol=1.e-5, atol=1.e-8):
    return abs(x-y) <= atol + rtol * abs(y)
    
def RM2EA(R):
    phi = 0.0
    if isClose(R[2,0],-1.0):
        theta = math.pi/2.0
        psi = math.atan2(R[0,1],R[0,2])
    elif isClose(R[2,0],1.0):
        theta = -math.pi/2.0
        psi = math.atan2(-R[0,1],-R[0,2])
    else:
        theta = -math.asin(R[2,0])
        cos_theta = math.cos(theta)
        psi = math.atan2(R[2,1]/cos_theta, R[2,2]/cos_theta)
        phi = math.atan2(R[1,0]/cos_theta, R[0,0]/cos_theta)
    return psi, theta, phi


R = np.array( [[-0.00447249, 0.27232334,   0.96219541],
 [ -0.99962192, -0.02732199,  0.00308629],
 [ 0.02712956,  -0.96181782,  0.27234257]]
)

roll, pitch, yaw = RM2EA(R)

print("roll:  {}\npitch: {}\nyaw:   {}".format(roll, pitch, yaw))




# import numpy as np
# from fractions import Fraction


# def rowReductionInverse(m):

#     mSize = len(m)                                                      # Get size of matrix
#     I = np.array([ [Fraction(0,1)] * mSize for i in range(mSize)])      # Create identity matrix, I, with the size of the mSize
#     for i in range(mSize):
#         I[i][i] = Fraction(1,1)
        
#     for col in range(mSize):                                            # Going through column by column

#         if m[col][col] == 0:                                            # If the diagonal value is 0. Find a row (within the column) with value and turn it to 1
#             rowWithValue = None
#             for irow in range(mSize):
#                 if m[irow][col] != 0:
#                     rowWithValue = irow
#                     break
            
#             var = m[rowWithValue][col]
#             m[col] = m[col] + (m[rowWithValue] / var)
#             I[col] = I[col] + (I[rowWithValue] / var)
        
#         else:                                                           # Else divide the row by itself to get 1 for the diagonal cell 
#             var = m[col][col]
#             m[col] = m[col] / var
#             I[col] = I[col] / var
        
#         for row in range(mSize):                                        # Go through the rest of the rows and zero them
            
#             if row == col:                                              # Ignore diagonals since its already processed
#                 continue
                
#             if m[row][col] == 0:
#                 continue

#             var = m[row][col]
#             m[row] = m[row] - (m[col] * var)
#             I[row] = I[row] - (I[col] * var)
#     return I

# matrix = [[-0.00447249, -0.99962192,  0.02712956, 0.0628641],
#  [ 0.27232334, -0.02732199, -0.96181782, -0.28950308],
#  [ 0.96219541,  0.00308629,  0.27234257,0.30773798],
#  [0,0,0,1]]

# matrix = np.asarray(matrix)

# print(rowReductionInverse(matrix))
