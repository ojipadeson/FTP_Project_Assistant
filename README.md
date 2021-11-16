# FTP_Project_Assistant

## Decription
Assistant for teacher assistant
Easily get all accuracy information of test.tsv or test.csv files from the FTP server of the project

## Run Example
```
python test_main.py --remote pj-1 
                    --host ***.**.***.***
                    --username ojipadeson
                    --password *******
                    --target .tsv,.csv
                    --ignore code
                    --standard ./standard_test_label.tsv
                    --header 0
                    --index 0
```