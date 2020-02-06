import numpy as np
import h5py
import json
import os
import pandas as pd

import tensorflow as tf
from tensorflow.keras.utils import multi_gpu_model
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Input, GRU, Dense, Embedding, Bidirectional, BatchNormalization, Concatenate
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.callbacks import CSVLogger, ModelCheckpoint
import wandb
from wandb.keras import WandbCallback

pd.set_option('display.max_columns', 10)

github_sha = os.getenv('GITHUB_SHA')
entity = os.getenv('WANDB_ENTITY')
project = os.getenv('WANDB_PROJECT')

print(f'Entity: {entity}')
print(f'Project: {project}')

wandb.init()
wandb.config.github_sha = github_sha
wandb.config.secondary_sha = ''

input_dir = "/data/"
out_dir = "/output/"

dataset = h5py.File('/data/dataset.hdf5', 'r')
with open("/data/metadata.json", "r") as f:
    meta = json.loads(f.read())

train_body_vecs, train_title_vecs, train_labels = (np.array(dataset['bodies']), 
                                                   np.array(dataset['titles']), 
                                                   np.array(dataset['targets']))

test_body_vecs, test_title_vecs, test_labels = (np.array(dataset['test_bodies']), 
                                                np.array(dataset['test_titles']), 
                                                np.array(dataset['test_targets']))

assert train_body_vecs.shape[0] == train_title_vecs.shape[0] == train_labels.shape[0]
assert test_body_vecs.shape[0] == test_title_vecs.shape[0] == test_labels.shape[0]

# build model architecture
body_emb_size = 50
title_emb_size = 50
batch_size = 900
epochs = 4

body_input = Input(shape=(meta['issue_body_doc_length'],), name='Body-Input')
title_input = Input(shape=(meta['issue_title_doc_length'],), name='Title-Input')

body = Embedding(meta['body_vocab_size']+2, body_emb_size, name='Body-Embedding')(body_input)
title = Embedding(meta['title_vocab_size']+2, title_emb_size, name='Title-Embedding')(title_input)

body = BatchNormalization()(body)
body = GRU(100, name='Body-Encoder')(body)

title = BatchNormalization()(title)
title = GRU(75, name='Title-Encoder')(title)

x = Concatenate(name='Concat')([body, title])
x = BatchNormalization()(x)
out = Dense(meta['num_classes'], activation='softmax')(x)

model = Model([body_input, title_input], out)

model.compile(optimizer=Adam(lr=0.001), 
              loss='sparse_categorical_crossentropy', 
              metrics=['accuracy'])

script_name_base = 'Issue_Labeler'
csv_logger = CSVLogger(out_dir + '{:}.log'.format(script_name_base))
model_checkpoint = ModelCheckpoint(out_dir + '{:}.epoch{{epoch:02d}}-val{{val_loss:.5f}}.hdf5'.format(script_name_base),
                                   save_best_only=True)


history = model.fit(x=[train_body_vecs, train_title_vecs], 
                    y=train_labels,
                    batch_size=batch_size,
                    epochs=epochs,
                    validation_data=[(test_body_vecs, test_title_vecs), test_labels], 
                    callbacks=[csv_logger, model_checkpoint,  WandbCallback()])


history_df = pd.DataFrame(history.history)
print(history_df.round(2))

best_val_loss = pd.DataFrame(history.history).val_loss.min()
best_val_acc = pd.DataFrame(history.history).val_accuracy.max()
wandb.log({'best_val_loss': best_val_loss})
wandb.log({'best_val_acc':best_val_acc})

# save artifacts
wandb.save(os.path.join(out_dir, '*'))
wandb.save('/data/metadata.json')
wandb.save(os.path.join(input_dir, '*.dpkl'))