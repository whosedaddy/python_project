# -*- coding: utf-8 -*-
"""
Created on Tue Dec 26 15:04:29 2017

@author: HP
"""

from PIL import Image

im = Image.open("randomcode_htm.gif")

#(转化为8进制像素)
im.convert("P")

#打印直方图颜色
print im.histogram()

his = im.histogram()
values = {}

for i in range(256):
    values[i] = his[i]
    
#以value值而不是key值排序
for j,k in sorted(values.items(), key = lambda x:x[1], reverse = True)[:20]:
    print j, k
    
im2= Image.new("P", im.size, 255)

for x in range(im.size[1]):
    for y in range(im.size[0]):
        pix = im.getpixel((y, x))
        if pix == 6 or pix == 33 or pix == 7 or pix == 31 or pix == 32 or pix == 46 or pix == 6 or pix == 44 or pix == 45 or pix == 47:
            im2.putpixel((y, x), 0)
            
im2.show()

inletter = False
foundletter = False
start = 0
end = 0

letters = []

for y in range(im2.size[0]):
    for x in range(im2.size[1]):
        pix = im2.getpixel((y, x))
        if pix != 255:
            inletter =True
    if foundletter == False and inletter == True:
        foundletter = True
        start = y
        
    if foundletter == True and inletter == False:
        foundletter = False
        end = y
        letters.append((start,end))
        
    inletter = False
    
print letters

import hashlib
import time

#切割
#count = 0
#for letter in letters:
    #m = hashlib.md5()
    #im3 = im2.crop(( letter[0], 0, letter[1], im2.size[1]))
    #m.update("%s%s"%(time.time(), count))
    #im3.save("./%s.gif"%(m.hexdigest()))
    #count += 1
    
import math
import os

class VectorCompare(object):
    #计算矢量大小
    def magnitude(self, concordance):
        total = 0
        for word, count in concordance.iteritems():
            total += count ** 2
        return math.sqrt(total)
    
    #计算矢量之间的cos值
    def relation(self, concordance1, concordance2):
        relevance = 0
        topvalue = 0
        for word, count in concordance1.iteritems():
            if concordance2.has_key(word):
                topvalue += count * concordance2[word]
        relevance = topvalue/(self.magnitude(concordance1) * \
                              self.magnitude(concordance2))
        return relevance
        
def buildvector(im):
    d1 = {}
    count = 0
    for i in im.getdata():
        d1[count] = i
        count += 1
    return d1

v = VectorCompare()

iconset = ['0','1','2','3','4','5','6','7','8','9','0','a','b','c','d',
           'e','f','g','h','i','j','k','l','m','n','o','p','q','r','s',
           't','u','v','w','x','y','z']

#加载训练集
imageset = []
for letter in iconset:
    for img in os.listdir('./iconset/%s/'%(letter)):
        temp = []
        if img != "Thumbs.db" and img != ".DS_Store":
            temp.append(buildvector(\
                    Image.open("./iconset/%s/%s"%(letter, img))))
        imageset.append({letter:temp})

count = 0
#切割
for letter in letters:
    m = hashlib.md5()
    im3 = im2.crop(( letter[0], 0, letter[1], im2.size[1]))
    m.update("%s%s"%(time.time(), count))
    im3.save("./%s.gif"%(m.hexdigest()))

    guess = []
    #进行比较
    for image in imageset:
        for x,y in image.iteritems():
            if len(y) != 0:
                guess.append((v.relation(y[0],buildvector(im3)),x))
                
    guess.sort(reverse = True)
    print "",guess[0]
    count += 1