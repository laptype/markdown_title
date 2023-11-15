#-*-coding:utf-8-*-
import re,sys
pattern='#+\s'

def ganMenu(filename):
  headId=0
  targetname="res.md"
  with open(targetname,'w+', encoding='utf-8') as f2:
      with open(filename,'r', encoding='utf-8') as f:
          for i in f.readlines():
            if not re.match(pattern,i.strip(' \t\n')):
              continue
            i=i.strip(' \t\n')
            head=i.split(' ')[0]

            str_t = '\t'*(len(head)-1)
            str_title = i[len(head):].strip(' \t\n')
            f2.write(f"{str_t}- [{str_title}](#{str_title})\n")
            headId+=1

if __name__ == '__main__':
    ganMenu("D:\lanbo\github\laptype_github_code\source\_posts\Leetcode\leetcode-basic-alg.md")