#!/usr/bin/env python3
"""fix-santamonica-pier.py — paint out the second, made-up pier on the horizon in the
brochure's Santa Monica sunset (page 10). Mike, 12 Nov 2026: "an additional pier out in the
ocean that needs to go". Coordinates are for the 3264 px wide page export.

Usage: python3 tools/fix-santamonica-pier.py p10.png p10-clean.png
brochure-crops.py uses p10-clean.png for the Santa Monica image when it exists.
"""
import cv2, numpy as np, sys
src,dst=sys.argv[1],sys.argv[2]
img=cv2.imread(src).astype(np.float32)
ox,oy=40,3050
out=img.copy()
X0,X1=ox+108,ox+640
Y0,Y1=oy+138,oy+254
sm=cv2.GaussianBlur(img,(0,0),6)
P=sm[Y0-6, X0:X1]                      # sky profile just above the patch (carries the sun glow)
P0,P1=P[0],P[-1]
t=np.linspace(0,1,X1-X0)[:,None]
for y in range(Y0,Y1):
    L=sm[y,X0-4]
    dL=L-P0
    if y < oy+190: dR=dL               # main pier railing/deck sits right of the patch on these rows
    else: dR=sm[y,X1+4]-P1
    k=min(1,(y-Y0)/((Y1-Y0)*0.55))     # glow profile fades out toward the horizon
    flat=L*(1-t)+(sm[y,X1+4] if y>=oy+190 else L)*t
    prof=P+dL*(1-t)+dR*t
    out[y,X0:X1]=prof*(1-k)+flat*k
ref=img[oy+40:oy+120, ox+150:ox+380]; g=ref-cv2.GaussianBlur(ref,(0,0),3)
H,W=Y1-Y0,X1-X0; out[Y0:Y1,X0:X1]+=np.tile(g,(H//g.shape[0]+1,W//g.shape[1]+1,1))[:H,:W]
mask=np.zeros(img.shape[:2],np.float32); mask[Y0:Y1,X0:X1]=1
mask=cv2.GaussianBlur(mask,(0,0),6)[...,None]
out=np.clip(img*(1-mask)+out*mask,0,255).astype(np.uint8)
m=np.zeros(out.shape[:2],np.uint8); cv2.rectangle(m,(ox+386,oy+66),(ox+414,oy+142),255,-1)
out=cv2.inpaint(out,m,12,cv2.INPAINT_NS)
cv2.imwrite(dst,out)
