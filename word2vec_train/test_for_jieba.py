#coding=utf-8
import jieba
import jieba.posseg as pseg

if __name__=='__main__':
    print 'hello world'

    # seg_list=jieba.cut("我在马路边，捡到5分钱。把它交到警察叔叔手里边",cut_all=False)
    # for mem in seg_list:
    #     print mem
    # print type(seg_list)

    # seg_list=jieba.cut_for_search("我在马路边，捡到5分钱。把它交到警察叔叔手里边")
    # for mem in seg_list:
    #     print mem

    seg_list=jieba.cut("我在马路边，捡到5分钱。把它交到警察叔叔手里边",cut_all=False)
    words=pseg.cut("我在马路边，捡到5分钱。把它交到警察叔叔手里边")
    for w in words:
        print w.word,' ',w.flag