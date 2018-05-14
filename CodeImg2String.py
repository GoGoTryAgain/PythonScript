import PIL.Image as Image
import os
from pytesser3 import image_to_string

#os.chdir('c:/Python27/Lib/site-packages/pytesser')#修改工作路径即可  

imgsrc = os.getcwd() + '\\code.PNG'
#灰化图片处理  
im = Image.open(imgsrc)  
  
imgry = im.convert('L')  
#二值化处理  


threshold = 100  
table = []  
for i in range(256):  
    if i < threshold:  
        table.append(0)  
    else:  
        table.append(1)  
out = imgry.point(table, '1')  

print('save out pic')
out.save('rgb.png')


#vcode = pytesseract.image_to_string(out)  


#print (vcode)  


txtcode = image_to_string(out)


print (u"\n识别出验证码文字为：",txtcode)