import os

import pandas as pd


def open_xsv(file: str,
             sep_tolerance=None,
             index=None,
             header=None,
             names=None):

    if sep_tolerance is None:
        sep_tolerance = ['\t', ',', ' ']
    for sep in sep_tolerance:
        data_loaded = pd.read_csv(file, sep=sep, index_col=index, header=header, names=names)
        if not data_loaded.empty:
            return data_loaded
    raise Exception('Cannot load (c/t)sv data. Expect separator {}'.format(sep_tolerance))


def accuracy_test(standard_file: str,
                  stu_strict_format=False,
                  auto_align='cut tail',
                  index=None,
                  header=None,
                  file_formats=None,
                  ignore=None):

    if ignore is None:
        ignore = ['./.idea', '__pycache__']
    ignore = ['./' + dir_name for dir_name in ignore]
    if file_formats is None:
        file_formats = ['.tsv', '.csv']
    test_tsv = open_xsv(standard_file, index=index, header=header)
    
    stu_index = []
    stu_acc = []
    for root, dirs, files in os.walk('./'):
        info_text = ''
        if not dirs and not root.startswith(tuple(ignore)):
            files_list = files.copy()
            for file in files_list:
                if file[-4:] not in file_formats:
                    files.remove(file)
            if not len(files):
                correct = 0
                info_text = 'No .tsv Files Found. SKIP'
            else:
                pred_tsv = open_xsv(os.path.join(root, files[0]), index=index, header=header, names=['prediction'])
    
                correct = 0
                if test_tsv.shape[0] < pred_tsv.shape[0]:
                    info_text = 'File Not auto_aligned, test:{} to pred:{} AUTO auto_aligned by {}'\
                        .format(test_tsv.shape[0], pred_tsv.shape[0], auto_align)
    
                    if auto_align == 'cut tail':
                        pred_tsv = pred_tsv[:- (pred_tsv.shape[0] - test_tsv.shape[0])]
                    else:
                        pred_tsv = pred_tsv[(pred_tsv.shape[0] - test_tsv.shape[0]):].reset_index(drop=True)
                elif test_tsv.shape[0] > pred_tsv.shape[0]:
                    info_text = 'File Not auto_aligned, test:{} to pred:{} COMPARE FRONT'\
                        .format(test_tsv.shape[0], pred_tsv.shape[0])
    
                for i in range(pred_tsv.shape[0]):
                    if pred_tsv['prediction'][i] == test_tsv['label'][i]:
                        correct += 1
    
            if stu_strict_format:
                if root[2:].startswith(tuple([str(i) for i in list(range(10))])):
                    print('{:20s} : {:.4f}    '.format(root[2:], correct / test_tsv.shape[0]), info_text)
            else:
                print('{:20s} : {:.4f}    '.format(root[2:], correct / test_tsv.shape[0]), info_text)
            if root[2:].startswith(tuple([str(i) for i in list(range(10))])):
                stu_index.append(root[2:])
                stu_acc.append(correct / test_tsv.shape[0])

    if len(stu_index) and len(stu_acc):
        stu_static = pd.Series(stu_acc)
        stu_info = pd.Series(stu_index)
        stu_df = pd.DataFrame({'info': stu_info, 'acc': stu_static})
        stu_df = stu_df.sort_values(by='acc', axis=0, ascending=False).reset_index(drop=True)
        stu_df.index += 1
        print('\n\n', stu_df.describe([.3, .5, .7, .9]), '\n\n')
        with pd.option_context('expand_frame_repr', False, 'display.max_rows', None):
            print(stu_df)
    return
