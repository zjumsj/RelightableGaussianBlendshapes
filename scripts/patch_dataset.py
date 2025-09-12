import os
import zipfile
import argparse

def find_valid_datasets(output_dir, dataset_list):
    valid_datasets = []
    for root, dirs, files in os.walk(output_dir):
        current_dir = os.path.basename(root)
        if current_dir in dataset_list:
            flag0 = os.path.isdir(os.path.join(root,"checkpoint"))
            flag1_0 = os.path.isdir(os.path.join(root,"images"))
            flag1_1 = os.path.isdir(os.path.join(root,"images.HQ"))
            if flag0 and (flag1_0 or flag1_1):
                valid_datasets.append((root, flag1_1))
                print('valid dir %s detected' % root)
            else:
                print('dir %s detected, but seems not valid, no checkpoints and images/images.HQ, skip...' % root)
    return valid_datasets

def process_zip_file(zip_path, valid_datasets):
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        all_files = zip_ref.namelist()
        for path_name, HR_flag in valid_datasets:
            subject = os.path.basename(path_name)
            extract_files = [file_path for file_path in all_files if file_path.startswith(subject) and not file_path.endswith('/')]
            savepath = os.path.join(path_name, "semantic.HQ" if HR_flag else "semantic")
            if os.path.exists(savepath):
                print('%s already exist, skip...' % savepath)
                continue
            os.makedirs(savepath, exist_ok=False)
            print('write %s ...' % savepath)
            for extract_file in extract_files:
                with zip_ref.open(extract_file) as source_file:
                    with open(os.path.join(savepath,os.path.basename(extract_file)),"wb") as target_file:
                        target_file.write(source_file.read())

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='patch dataset')
    parser.add_argument('-i','--input',type=str, required=True, help='source file (.zip)')
    parser.add_argument('-o','--output', type=str, required=True, help='folder to find dataset to patch.')

    args, unknown = parser.parse_known_args()
    if len(unknown) != 0:
        print(unknown)
        exit(-1)

    if not os.path.exists(args.input):
        print('input %s not found. exit...' % args.input)
        exit(1)

    if not os.path.exists(args.output):
        print('output %s not found. exit...' % args.output)
        exit(1)

    dataset_list = [
        "bala", "biden", "justin", "malte_1", "marcel", "nf_01", "nf_03", "wojtek_1",
        "subject1", "subject2", "subject3", "subject4", "subject5"
    ]

    valid_datasets = find_valid_datasets(args.output, dataset_list)
    if len(valid_datasets) == 0:
        print('No valid dataset find. exit...')
        exit(1)

    process_zip_file(args.input, valid_datasets)
    print('done.')
    
    
