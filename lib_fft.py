# FFT related tools library of GEOS627 inverse course
# Coded by Yuan Tian at UAF 2021.01
import numpy as np
import scipy
import matplotlib.pyplot as plt


def xy2distance_row1(nx,ny):
    ix0 = np.arange(nx)
    iy0 = np.arange(ny)

    # generate integer ix and iy vectors
    [iX,iY] = np.meshgrid(ix0,iy0)
    ix = iX.flatten(order='F')
    iy = iY.flatten(order='F')

    n = nx*ny
    xref = ix[0]
    yref = iy[0]
    iD2row1 = (xref-ix)**2 + (yref-iy)**2
    return np.sqrt(iD2row1),ix0,iy0

def xy2distance(nx,ny):
    # integer index vectors
    # NOTE: these start with 0 for convenience in the FFT algorithm
    ix0 = np.arange(nx)
    iy0 = np.arange(ny)

    # generate integer ix and iy vectors
    [iX,iY] = np.meshgrid(ix0,iy0)
    ix = iX.T.flatten(order='F')
    iy = iY.T.flatten(order='F')
    MX,MY=np.meshgrid(ix,iy)
    iD=np.sqrt((MX-MX.T)**2+(MY-MY.T)**2)

    return iD,ix0,iy0

def k_of_x(x):
    N      = np.max(x.shape)
    dx     = x[1]-x[0]
    dk     = (2*np.pi)/(N*dx)
    inull  = N/2
    k      = dk*(np.linspace(1,N,N)-inull)
    return k

def x_of_k(k):
    N      = np.max(k.shape)
    dk     = k[1]-k[0]
    dx     = (2*np.pi)/(N*dk)
    x      = dx*(np.linspace(1,N,N)-1)
    return x


def mhfft2(x,y,f):
    # 2D Fast Fourier Transform of (x,y,f) into (k,l,ft).  The length of 
    # x,y  and f must be an even number, preferably a power of two.  The index of
    # the zero mode is inull=jnull=N/2.

    # Everything is assumed to have been generated by meshgrid, so that
    # f is indexed f(y,x)

    Nx         = np.max(x.shape)
    Ny         = np.max(y.shape)
    k          = k_of_x(x)
    l          = k_of_x(y)
    Periodx    = Nx*(x[1]-x[0])
    Periody    = Ny*(y[1]-y[0])
    inull      = Nx/2
    jnull      = Ny/2
    ft         = (Periodx/Nx)*(Periody/Ny)*np.roll(np.roll(np.fft.fft2(f),int(jnull-1),axis=0),int(inull-1),axis=1)
    return k,l,ft
def grf2(k,m,C,n,*argv):
    Nx         = np.max(k.shape)
    Ny         = np.max(m.shape)
    dk=k[1]-k[0]
    dm=m[1]-m[0]
    Periodx    =2*np.pi/dk
    Periody    =2*np.pi/dm
    Cmtx=np.repeat(C[:, :, np.newaxis], n, axis=2)
    
    # if nargin==6:
    #     disp('grf2mod.m: using the provided Gaussian random vectors (A and B)')
    # else:
    if argv:
        A=argv[0]
        B=argv[1]
    else:
        A = np.random.randn(Ny,Nx,n)   # N(0,1) random variables
        B = np.random.randn(Ny,Nx,n); 
    phi=np.sqrt(Periodx*Periody*Cmtx/2)*(A+B*1j)
    phi[np.isnan(phi)]=0
    return phi, A,B
def mhifft2(k,l,ft,rflag):
    # 2D Fast Fourier Transform of (x,y,f) into (k,l,ft).  The length of 
    # x,y  and f must be an even number, preferably a power of two.  The index of
    # the zero mode is inull=jnull=N/2.

    # Everything is assumed to have been generated by meshgrid, so that
    # f is indexed f(y,x)

    Nx         = np.max(k.shape)
    Ny         = np.max(l.shape)
    x          = x_of_k(k)
    y          = x_of_k(l)
    Periodx    = Nx*(x[1]-x[0])
    Periody    = Ny*(y[1]-y[0])
    inull      = Nx/2
    jnull      = Ny/2
    f         = (Nx/Periodx)*(Ny/Periody)*np.fft.ifftn(np.roll(np.roll(ft,-int(jnull-1),axis=0),-int(inull-1),axis=1),axes=(0,1))
    if rflag==1:
        f=np.real(f)
    return x,y,f
