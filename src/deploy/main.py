import json
import os
import sys

import dill as dpickle
import tensorflow as tf
import wandb


class IssueLabeler:
    def __init__(self, 
                 body_text_preprocessor, 
                 title_text_preprocessor, 
                 model, 
                 class_names=['bug', 'feature_request', 'question']):
        """
        Parameters
        ----------
        body_text_preprocessor: ktext.preprocess.processor
            the text preprocessor trained on issue bodies
        title_text_preprocessor: ktext.preprocess.processor
            text preprocessor trained on issue titles
        model: tensorflow.keras.models
            a keras model that takes as input two tensors: vectorized 
            issue body and issue title.
        class_names: list
            class names as they correspond to the integer indices supplied to the model. 
        """
        self.body_pp = body_text_preprocessor
        self.title_pp = title_text_preprocessor
        self.model = model
        self.class_names = class_names
        
    
    def get_probabilities(self, body:str, title:str):
        """
        Get probabilities for the each class. 
        
        Parameters
        ----------
        body: str
           the issue body
        title: str
            the issue title
            
        Returns
        ------
        Dict[str:float]
        
        Example
        -------
        >>> issue_labeler = IssueLabeler(body_pp, title_pp, model)
        >>> issue_labeler.get_probabilities('hello world', 'hello world')
        {'bug': 0.08372017741203308,
         'feature': 0.6401631832122803,
         'question': 0.2761166989803314}
        """
        # transform raw text into array of ints
        vec_body = self.body_pp.transform([body])
        vec_title = self.title_pp.transform([title])
        
        # get predictions
        probs = self.model.predict(x=[vec_body, vec_title]).tolist()[0]
        
        return {k:v for k, v in zip(self.class_names, probs)}

# Build the Issue Labeler In The Global Scope
#############################################
api = wandb.Api()
run = api.run('{}/{}/{}'.format(os.getenv('WANDB_ENTITY'),
                                os.getenv('WANDB_PROJECT'),
                                os.getenv('WANDB_RUN_ID')))

# Fetch and load best model for run id
run.file('model-best.h5').download(replace=True, root='/tmp')
model = tf.keras.models.load_model('/tmp/model-best.h5')

# Download data pre-processing artifacts
run.file('title_pp.dpkl').download(replace=True, root='/tmp')
run.file('body_pp.dpkl').download(replace=True, root='/tmp')

# Load data pre-processing artifacts into memory
with open('/tmp/title_pp.dpkl', 'rb') as f:
    title_pp = dpickle.load(f)

with open('/tmp/body_pp.dpkl', 'rb') as f:
    body_pp = dpickle.load(f)

# instantiate the IssueLabeler object
issue_labeler = IssueLabeler(body_text_preprocessor=body_pp,
                             title_text_preprocessor=title_pp,
                             model=model)


def predict(request):
    request_json = request.get_json(silent=True)
    if 'body' not in request_json or 'title' not in request_json:
        return "Error: Request must contain the fields `body` and `title`"
    body = request_json['body']
    title = request_json['title']

    try:
        predictions = issue_labeler.get_probabilities(body=f"{body}", 
                                                      title=f"{title}")
    except:
        return f"Error making prediction: {sys.exc_info()[0]}"

    return json.dumps(predictions)
