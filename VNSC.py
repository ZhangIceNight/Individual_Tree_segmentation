from sklearn.cluster import KMeans,MeanShift,estimate_bandwidth
from sklearn.preprocessing import normalize
from sklearn.neighbors import NearestNeighbors
import numpy as np
from numpy import linalg as LA
import gc
import csv

############################## Nyström谱聚类实现 ########################################
def SpectralNystrom(X,g):  
    """
    实现基于Nyström方法的谱聚类算法
    参数:
        X: 输入数据矩阵
        g: 聚类数量的上限
    """
    nXx = np.shape(X)[0] 
    std_dev = 10    # 高斯核函数的标准差
    knn = 40        # K近邻数量
    # 构建KNN搜索树
    nbrs = NearestNeighbors(n_neighbors=knn, algorithm="kd_tree").fit(np.array(X[:,:2]))  
    distances, indices = nbrs.kneighbors(np.array(X[:,:2])) 
    
    # 计算高度差异
    distances0 = np.zeros((knn,))
    for jj in range(nXx):
        l1 = X[jj,2]
        l2 = X[indices[jj,:],2]
        deta_l = abs(l1-l2)
        distances0 = np.vstack((distances0,deta_l))
    distances0 = distances0[1:(nXx+1),:]  
    
    # 构建相似度图
    for j in range(knn):    
         distances[:,j] = distances[:,j]*distances[:,j]*X[:,3]*X[indices[:,j],3] 
         distances0[:,j] = distances0[:,j]*distances0[:,j]*X[:,3]*X[indices[:,j],3]    
     
    # 计算高斯核相似度
    distances = np.exp(-distances/std_dev)*np.exp(-distances0/std_dev)    
    del X
    gc.collect()

    #******************************* KNNS采样 *******************************************#
    # 计算每个点的权重和
    sumw = np.sum(distances,axis=1)  
    sumw = np.vstack((sumw,[0 for i in range(nXx)])).T  
    idsumw = np.lexsort([-sumw[:,0]])   
    X1,X2,AA,BB = [],[],[],[]  # X1存储采样点，X2存储剩余点
    
    # 基于权重进行采样
    for ii in range(nXx):
        i = idsumw[ii]
        if sumw[i,1] == 0: 
            X1.extend([i])  
            sumw[i,1] = -1
            sim1 = [0 for k1 in range(len(X1))]
            sim2 = [0 for k2 in range(len(X2)+knn)] 
            for j in range(knn):
                if indices[i,j] in X1:
                    id1 = X1.index(indices[i,j]) 
                    sim1[id1] = distances[i,j]
                    sim2.pop()  
                elif indices[i,j] in X2:
                    id2 = X2.index(indices[i,j])
                    sim2[id2] = distances[i,j]
                    sim2.pop()
                else:
                    X2.extend([indices[i,j]])  
                    sim2[len(X2)-1] = distances[i,j]
                    sumw[indices[i,j],1] = -1
            AA.append(sim1)
            BB.append(sim2)
            
    del distances,indices
    gc.collect() 

    # 构建近似特征向量
    samples = len(X1)
    remains = len(X2)
    A = np.eye(samples)  # A矩阵：采样点之间的相似度
    B = np.zeros((samples,remains))  # B矩阵：采样点与剩余点之间的相似度
    for i in range(samples):
        A[i,:(i+1)] = AA[i]
        B[i,:len(BB[i])] = BB[i]
    del AA,BB
    gc.collect()

    #********************************** 特征分解 *************************************#
    idx = np.hstack((X1,X2))
    sumw = sumw[idx,0]
    d = np.power(sumw,-0.5)  # 计算度矩阵的逆平方根
    dd = np.dot(d.reshape((len(d),1)),d.reshape((1,len(d))))
    A = A*dd[:samples,:samples]
    B = B*dd[:samples,samples:]
    detA = LA.det(np.sqrt(A))   
    if detA>0:
        Asi = LA.inv(np.sqrt(A))   
    else:
        Asi = LA.pinv(np.sqrt(A))   # 如果矩阵奇异，使用伪逆
    Q = A+np.dot(np.dot(np.dot(Asi,B),B.T),Asi)  
    eigvals, eigvecs = LA.eig(Q)   # 特征分解
    Lamda = np.diag(np.power(eigvals, -0.5))
    V = np.dot(np.dot(np.dot(np.vstack((A,B.T)),Asi),eigvecs),Lamda)
    
    #***************************** 聚类分割 *************************************#
    # 自适应确定聚类数
    eeigval = sorted(eigvals)
    if g==1 or len(eeigval)-1<g:
        g = len(eeigval)-1
    eeigval = np.array(eeigval)
    g1 = int(2*g/4)   
    gap = eeigval[(g1+1):(g+1)]-eeigval[g1:g] 
    sk0 = np.argsort(-gap)[0]
    sk = sk0+g1 
    idsk = np.argsort(-eigvals)[:sk]  
    k_biggest_eigenvectors = normalize(np.real(V[:, idsk])) 
    # 执行K-means聚类
    labels = KMeans(n_clusters=int(sk)).fit_predict(k_biggest_eigenvectors)
    sk = len(np.unique(labels))
    return sk,idx,labels

################################## 计算单木参数 ###########################################
def Parameter(C,labels,total):
    """
    计算每棵树的参数（位置、树冠大小等）
    参数:
        C: 点云坐标
        labels: 聚类标签
        total: 树木总数
    """
    indices = np.argsort(labels)
    labels = labels[indices]
    C = C[indices, :]
    subid = []
    for i in range(total):
        subid.extend([labels.tolist().index(i)])  
    bio = []
    # 计算每棵树的参数
    for j in range(total):
        if j==(total-1):
            final_subX = C[subid[j]:,:]
        else:
            final_subX = C[subid[j]:subid[j+1],:]
        # 获取边界点
        index_xmin = np.lexsort([final_subX[:,0]])[0]  
        index_xmax = np.lexsort([-final_subX[:,0]])[0] 
        index_ymin = np.lexsort([final_subX[:,1]])[0]  
        index_ymax = np.lexsort([-final_subX[:,1]])[0] 
        index_zmax = np.lexsort([-final_subX[:,2]])[0] 
        # 计算树木参数
        x = final_subX[index_zmax,0]
        y = final_subX[index_zmax,1]
        xmin = final_subX[index_xmin,0]
        xmax = final_subX[index_xmax,0]
        ymin = final_subX[index_ymin,1]
        ymax = final_subX[index_ymax,1]
        bio.append([j,x,y,(xmax-xmin+ymax-ymin)/4,final_subX[index_zmax,2]]) 

    return bio
    
########################### 体素化与Nyström谱聚类调用 #############################
def VoxelNystromSC(P,xid,gap,path):
    """
    执行体素化和Nyström谱聚类
    参数:
        P: 点云数据
        xid: 文件标识符
        gap: 聚类数量上限
        path: 输出路径
    """
    zd = 6  # z轴缩放因子
    a = np.array([1,1,zd])
    P = P/a  # 点云归一化
    nP = np.shape(P)[0]  
    # 计算点云边界
    x0 = P[np.lexsort([P[:,0]])[0],0]
    x1 = P[np.lexsort([-P[:,0]])[0],0]
    y0 = P[np.lexsort([P[:,1]])[0],1]
    y1 = P[np.lexsort([-P[:,1]])[0],1]
    # 估计密度
    den0 = round(nP/((x1-x0)*(y1-y0)))  
    # 执行均值漂移聚类进行体素化
    bandwidth = estimate_bandwidth(P, quantile=den0/nP)
    ms = MeanShift(bandwidth=bandwidth, bin_seeding=True) 
    ms.fit(P) 
    labels = ms.labels_  
    
    # 获取聚类中心
    cluster_centers = ms.cluster_centers_ 
    cluster_centers = np.hstack((cluster_centers,[[labels.tolist().count(i)] for i in range(np.shape(cluster_centers)[0])]))

    # 执行Nyström谱聚类
    [k,mlabels,Slabels] = SpectralNystrom(cluster_centers,gap)  
    idclu = np.argsort(mlabels)  
    Slabels = Slabels[idclu]  
    # 更新点云标签
    for i in range(nP):
        j = labels[i]
        labels[i] = Slabels[j]
    del cluster_centers,Slabels,mlabels
    gc.collect()
    
    # 恢复原始尺度
    P = P*a 
    PP = np.column_stack((P,labels))
    PP0 = PP[np.lexsort(PP.T)]
    # 计算树木参数
    SSbio = Parameter(PP0[:,:3],PP0[:,3],k)  
    SSbio = np.array(SSbio)
   
    # 保存分割结果
    out1 = open(path+"\\results\\Data_seg_%s.csv"%(xid),'w',newline='\n')
    csv_write1 = csv.writer(out1,dialect='excel')
    csv_write1.writerow(('x','y','z','label'))
    for i in range(np.shape(PP0)[0]):
        csv_write1.writerow((PP0[i,0],PP0[i,1],PP0[i,2],PP0[i,3]))
       
    # 保存树木参数
    out2 = open(path+"\\results\\Parameter_%s.csv"%(xid),'w',newline='\n')
    csv_write2 = csv.writer(out2,dialect='excel')
    csv_write2.writerow(('TreeID','Position_X','Position_Y','Crown','Height'))
    for i in range(np.shape(SSbio)[0]):
        csv_write2.writerow((SSbio[i,0],SSbio[i,1],SSbio[i,2],SSbio[i,3],SSbio[i,4]))



   
    
