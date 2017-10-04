#coding=utf-8
import os
import numpy as np
from gensim.models import Word2Vec

def write2txt(str_list,fname):
    '''
    字符串文字写入文件
    :param str_list:
    :param fname:
    :return:
    '''
    writer = open(fname, 'w')
    for line in str_list:
        # print '--'+line
        # line=line.replace('\n','')
        writer.write(line+'\n')
    writer.close()

def raw_data_merge(path):
    '''
    合并未编码的数据
    :param path:
    :return:
    '''
    data_test=list()
    data_train=list()
    for fname in os.listdir(path):
        fpath=path+fname
        reader=open(fpath,'r')
        # for line in reader.readlines():
        #     line=line.replace('\n','')
        #     print line.split(',')[-2]
        if fname.find('test')==-1:  #合并 train数据集
            for line in reader.readlines():
                line=line.replace('\n','').replace(chr(13),'')
                # print '==',line
                # if not line:
                #     print 'yes,it is empty'
                data_train.append(line)
        else:   #合并 test数据集
            for line in reader.readlines():
                line = line.replace('\n', '').replace(chr(13), '')
                data_test.append(line)
    #合并的数据集写入文件
    if path.find('data_A')!=-1:
        pass
        fname_train = path.replace('data_A/', 'A_') + 'merge_train.txt'
        fname_test = path.replace('data_A/', 'A_')+ 'merge_test.txt'
        write2txt(data_train, fname_train)
        write2txt(data_test, fname_test)
    elif path.find('data_B')!=-1:
        pass
        fname_train = path.replace('data_B/', 'B_') + 'merge_train.txt'
        fname_test = path.replace('data_B/', 'B_') + 'merge_test.txt'
        write2txt(data_train, fname_train)
        write2txt(data_test, fname_test)
    else:
        print 'not A or B'


def label_mapping(fname_train):
    '''
    生成标签映射
    :param fname_train:
    :return:
    '''
    label_dict=dict()
    #整理字典
    reader=open(fname_train,'r')
    for line in reader.readlines():
        line=line.replace('\n','')
        label=line.split(',')[-2].replace(' ','')
        if label not in label_dict:
            label_dict[label]=len(label_dict)+1
            # print label

    #写入文件中
    fname_save='raw_data/label_mapping_AB.txt'
    writer=open(fname_save,'w')
    for k,v in sorted(label_dict.items()):
        line=str(k)+'\t'+str(v)
        writer.write(line+'\n')
        # print k,'--',v
    writer.close()

def txt2dict(fname,sep='\t'):
    '''
    返回标签映射字典
    :param fname:
    :param sep:
    :return:
    '''

    label_dict=dict()
    reader=open(fname,'r')
    for line in reader.readlines():
        line=line.replace('\n','')
        temps=line.split(sep)
        label=temps[0].replace(' ','')
        num=float(temps[1].replace(' ',''))
        label_dict[label]=num
    reader.close()

    return label_dict

def w2v_encode(fname,w2v_model,label_dict,sep=','):
    data_x=list()
    data_y=list()
    reader=open(fname,'r')
    for line in reader.readlines():
        line=line.replace('\n','')
        temps=line.split(sep)
        sentence=temps[-1]
        label=temps[-2]

        # print sentence,'    ',
        sample_x=list()
        for word in sentence.split(' '):
            word=unicode(word, "utf-8")
            if word in w2v_model:
                # print word
                sample_x.append(w2v_model[word])
        # if len(sample_x)!=0:
        #     print 'some one is not 0!!'
        #     print word,'-',
        # print '\n====================================='
        # print ''
        sample_y=0
        if label in label_dict:
            sample_y=label_dict[label]
        else:
            print label,' is not in the label_dict'

        data_x.append(sample_x)
        data_y.append(sample_y)
    print '============================================='
    print len(data_x[0])
    print '-------------'
    print '============================================='

    np.save(fname.replace('.txt','_x.npy').replace('raw_data','w2v_data'),data_x)
    np.save(fname.replace('.txt','_y.npy').replace('raw_data','w2v_data'),data_y)


if __name__ == '__main__':
    print 'Xuyuhong_dataprocess is running...'

    # #合并A数据集
    # path='raw_data/data_A/'
    # raw_data_merge(path)
    #
    # # 合并B数据集
    # path = 'raw_data/data_B/'
    # raw_data_merge(path)

    # #将标签映射为数字
    # fname_train='raw_data/data_A/merge_train.txt'
    # label_mapping(fname_train)

    # 读入标签映射生成字典
    fname_label_mapping = 'raw_data/label_mapping_AB.txt'
    label_dict=txt2dict(fname_label_mapping)
    #载入词向量模型
    fname_w2v='model/weibo10G_w2v_dim50/merge_10G_weibo_50.model'
    w2v_model=Word2Vec.load(fname_w2v)
    # w2v_model=None
    # print w2v_model['世界杯']
    #编码
    fname_list = ['raw_data/A_merge_train.txt', 'raw_data/A_merge_test.txt',
                  'raw_data/B_merge_train.txt', 'raw_data/B_merge_test.txt']
    for fname in fname_list:
        w2v_encode(fname,w2v_model,label_dict)
