# FTP_Project_Assistant

## Decription
For machine learning related teacher assistant to easily get all accuracy information of students' test.tsv

## Run Example
```
python test_main.py --remote **machine_learning_project**
                    --local **local_dir_path**
                    --host ***.**.***.***
                    --username ojipadeson
                    --password *******
                    --target .tsv,.csv
                    --ignore code
                    --standard ./standard_test_label.tsv
                    --header 0
                    --index 0
```

## Option

---

**```target```  -- the target file format.**

For example, if ```Report.pdf``` and ```Prediction.csv``` are needed,
you have to type ```.csv,.pdf```.

* DON'T TYPE ```''``` to generate your input as a string
* USE ```,``` to split your file format, NO ```SPACE```

---

**```ignore```  -- the directory that you will ignore.**

For Example, ```--ignore code``` means you won't search or copy directory named as ```'code'```

---

**```standard```  -- the path of standard answer in local directory.**

---

**```header``` & ```index```  -- the table format of ```test.csv(.tsv)```**

For example, ```--header 0 --index 0``` means your table in test file should be like below:

index   |	prediction
----    |   ----
0	|   1
1	|   1
2	|   0
3	|   1


## File Format on FTP Server
```
FTP Server
│
├─pj-1
│  ├─stu_1
│  │   ├─code.zip
│  │   ├─report.pdf
│  │   └─test.tsv
│  ├─stu_2
│  │   ├─Code.zip
│  │   ├─My_report.pdf
│  │   └─test.csv
│  ├─stu_3
│  │   ├─nlp_pj_code.zip
│  │   ├─Report_2021.pdf
│  │   └─result.tsv
│  ├─...
│  │   └─...
│  └─...
│
├─pj-2
│  ├─stu_1
│  │   ├─code.zip
│  │   ├─report.pdf
│  │   └─test.tsv
│  ├─...
│  │   └─...
│  ...
│
└─...
```
On the FTP server, the directory tree should be like above.