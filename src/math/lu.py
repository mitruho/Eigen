import numpy as np

def lu(A):
    "Compute LU decomposition of matrix A."
    A = np.array(A)
    m,n = A.shape
    L = np.eye(m)
    U = A.copy()
    pivot = 0
    for j in range(0,n):
        # Check if the pivot entry is 0
        if U[pivot,j] == 0:
            if np.any(U[pivot+1:,j]):
                # LU decomposition does not exist if entries below 0 pivot are nonzero
                raise ValueError
            else:
                continue
        for i in range(pivot+1,m):
            c = -U[i,j]/U[pivot,j]
            U[i,:] = c*U[pivot,:] + U[i,:]
            L[i,pivot] = -c
        pivot += 1
    return L,U