import pandas as pd
from sklearn.model_selection import train_test_split
from ktext.preprocess import processor
import dill as dpickle
import numpy as np
import h5py
import json

df = pd.concat([pd.read_csv(f'https://storage.googleapis.com/codenet/issue_labels/00000000000{i}.csv.gz')
                for i in range(1)])

print('class name to integer check:')
print(df[['class_int', 'c_bug', 'c_feature', 'c_question']].groupby('class_int').max())

#split data into train/test
traindf, testdf = train_test_split(df, test_size=.15, random_state=0)
# Clean, tokenize, and apply padding / truncating such that each document length = 75th percentile for the dataset.
#  also, retain only the top keep_n words in the vocabulary and set the remaining words
#  to 1 which will become common index for rare words 

train_body_raw = traindf.body.tolist()
train_title_raw = traindf.title.tolist()

# process the issue body data
body_pp = processor(.75, keep_n=8000)
train_body_vecs = body_pp.fit_transform(train_body_raw)

# process the title data
title_pp = processor(.75, keep_n=4500)
train_title_vecs = title_pp.fit_transform(train_title_raw)

# apply transformations to test data
test_body_raw = testdf.body.tolist()
test_title_raw = testdf.title.tolist()

test_body_vecs = body_pp.transform_parallel(test_body_raw)
test_title_vecs = title_pp.transform_parallel(test_title_raw)


# extract labels
train_labels = np.expand_dims(traindf.class_int.values, -1)
test_labels = np.expand_dims(testdf.class_int.values, -1)
num_classes = len(set(train_labels[:, 0]))

# Check shapes
# the number of rows in data for the body, title and labels should be the same for both train and test partitions
assert train_body_vecs.shape[0] == train_title_vecs.shape[0] == train_labels.shape[0]
assert test_body_vecs.shape[0] == test_title_vecs.shape[0] == test_labels.shape[0]
assert num_classes == 3

f = h5py.File('/data/dataset.hdf5', 'w')
f.create_dataset('/titles', data=train_title_vecs)
f.create_dataset('/bodies', data=train_body_vecs)
f.create_dataset('/targets', data=train_labels)

f.create_dataset('/test_titles', data=test_title_vecs)
f.create_dataset('/test_bodies', data=test_body_vecs)
f.create_dataset('/test_targets', data=test_labels)
f.close()


with open("/data/metadata.json", "w") as f:
    meta = {
        'body_vocab_size': body_pp.n_tokens,
        'title_vocab_size': title_pp.n_tokens,
        'issue_body_doc_length': train_body_vecs.shape[1],
        'issue_title_doc_length': train_title_vecs.shape[1],
        'num_classes': num_classes,
    }
    f.write(json.dumps(meta))

print(f'Metadata:\n {meta}')

# Save the preprocessor
with open('/data/body_pp.dpkl', 'wb') as f:
    dpickle.dump(body_pp, f)

with open('/data/title_pp.dpkl', 'wb') as f:
    dpickle.dump(title_pp, f)