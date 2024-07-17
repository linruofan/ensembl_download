# ensembl_download  
从ensembl中下载序列的脚本，有一个简陋的可视化界面，源代码文件![download_seq_ensembl.py](download_seq_ensembl.py)  

### 输入文件  
输入文件格式需要是excel文件，**第一行是表名，第二行是列名，第三行及以下为序列名**  
示例excel文件![examplefile.xlsx](examplefile.xlsx)  

### 输出  
每个序列以fasta格式保存在单独的文件中，每一列的序列会下载到同一个以第二行列名命名的文件夹里
