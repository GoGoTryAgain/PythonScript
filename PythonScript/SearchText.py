import os
import sys
import io
import re


#sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='gb18030')

# 如果需要搜索除了以下的额外的文件格式，请在后面追加,如果需要所有的文件都搜，则更改fileAllTyoes 为 True,默认未False
filetypes = '.c .h .alf .txt .doc .pdf .docx '
fileAllTypes = False;
	



print('serch start now, please wait..\r\n')

if len(sys.argv) is 1 :
    print('Error!!! :check your input!!!,Please enter search text!!!\r\n')
    print('warn : run as "python searchline.py  C:\   helloworld"\r\n')
    sys.exit()

elif len(sys.argv) is 2 :
    path = os.getcwd()
    matchline = sys.argv[1] 
    
elif  len(sys.argv) is 3 :
    path = sys.argv[1]
    matchline = sys.argv[2] 

elif len(sys.argv) is 4 :
    fileAllTypes = argv[3]

files = os.walk(path)

for parent , dirnames,filenames in os.walk(path):
    for filename in filenames:
        if fileAllTypes or re.match(r'.*' + os.path.splitext(filename)[1], filetypes):
            #print('open file is ' + os.path.join(parent,filename)+ '\r\n')
            f = open(os.path.join(parent,filename),errors = 'ignore')
            lineNum = 0
            iter_f = iter(f)
            for line in iter_f:  # 遍历文件，一行行遍历
                lineNum = lineNum + 1
                if re.match(r'.*' + matchline, line):
                    print('search successful !!! \r\npath is ' + os.path.join(parent,filename))
                    print('And the line is ' , lineNum)
                    print('the content is :     ' + line)
            f.close()

print('\r\nserch finish')


