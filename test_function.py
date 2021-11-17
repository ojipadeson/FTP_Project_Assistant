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


def clean_list(files: list,
               file_formats: list):

    files_list = files.copy()
    for file in files_list:
        if file[-4:] not in file_formats:
            files.remove(file)
    return files


def print_acc_dataframe(stu_index: list,
                        stu_acc: list,
                        percentile: list):

    if len(stu_index) and len(stu_acc):
        stu_static = pd.Series(stu_acc)
        stu_info = pd.Series(stu_index)
        stu_df = pd.DataFrame({'info': stu_info, 'acc': stu_static})
        stu_df = stu_df.sort_values(by='acc', axis=0, ascending=False).reset_index(drop=True)
        stu_df.index += 1
        print('\n\n', stu_df.describe(percentile), '\n\n')
        with pd.option_context('expand_frame_repr', False, 'display.max_rows', None):
            print(stu_df)
    else:
        print('No accuracy information. Cannot create leaderboard.')
    return


def auto_align_function(test_file: pd.DataFrame,
                        standard_file: pd.DataFrame,
                        align: str):

    if align is 'cut tail':
        test_file = test_file[:- (test_file.shape[0] - standard_file.shape[0])]
    else:
        test_file = test_file[(test_file.shape[0] - standard_file.shape[0]):].reset_index(drop=True)
    return test_file


def correct_count(test_file: pd.Series,
                  standard_file: pd.Series):

    compare_range = test_file.shape[0]
    error_rate = test_file.compare(standard_file[:compare_range]).shape[0] / standard_file.shape[0]
    return 1 - error_rate


def accuracy_test(standard_file: str,
                  local_dir_path: str,
                  auto_align='cut tail',
                  index=None,
                  header=None,
                  file_formats=None,
                  ignore=None):

    if ignore is None:
        ignore = ['.idea', '__pycache__', '.git']
    ignore = [local_dir_path + '/' + dir_name for dir_name in ignore]
    if file_formats is None:
        file_formats = ['.tsv', '.csv']
    test_tsv = open_xsv(standard_file, index=index, header=header)

    stu_index = []
    stu_acc = []
    for root, dirs, files in os.walk(local_dir_path + '/'):
        info_text = ''
        if not dirs and not root.startswith(tuple(ignore)):
            files = clean_list(files, file_formats)
            if not len(files):
                accuracy = 0
                info_text = 'No .tsv Files Found. SKIP'
            else:
                pred_tsv = open_xsv(os.path.join(root, files[0]), index=index, header=header, names=['prediction'])
                if test_tsv.shape[0] < pred_tsv.shape[0]:
                    info_text = 'File Not auto_aligned, test:{} to pred:{} AUTO auto_aligned by {}' \
                        .format(test_tsv.shape[0], pred_tsv.shape[0], auto_align)
                    pred_tsv = auto_align_function(pred_tsv, test_tsv, auto_align)
                elif test_tsv.shape[0] > pred_tsv.shape[0]:
                    info_text = 'File Not auto_aligned, test:{} to pred:{} COMPARE FRONT' \
                        .format(test_tsv.shape[0], pred_tsv.shape[0])

                accuracy = correct_count(pred_tsv['prediction'], test_tsv['label'])

            print('{0:{1}>20}'.format(root[len(local_dir_path) + 1:], chr(12288)), end='')
            print(':      {:.4f}    '.format(accuracy), info_text)
            if root[len(local_dir_path) + 1:].startswith(tuple([str(i) for i in list(range(10))])):
                stu_index.append(root[len(local_dir_path) + 1:])
                stu_acc.append(accuracy)

    print_acc_dataframe(stu_index, stu_acc, [.3, .5, .7, .9])
    return
