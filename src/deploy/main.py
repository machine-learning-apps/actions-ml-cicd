import os

import tensorflow as tf
import wandb

model = None

def predict(request):
    global model
    if not model:
        api = wandb.Api()
        run = api.run('{}/{}/{}'.format(os.getenv('WANDB_ENTITY'), os.getenv('WANDB_PROJECT'), os.getenv('WANDB_RUN_ID')))
        run.file('model-best.h5').download(replace=True, root='/tmp')
        model = tf.keras.models.load_model('/tmp/model-best.h5')
    return model.to_json()
