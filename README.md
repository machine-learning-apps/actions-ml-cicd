# A Collection of GitHub Actions That Facilitate MLOps

Materials that accompany the talk [MLOps with GitHub Actions & Kubernetes](https://youtu.be/Ll50l3fsoYs).

## A Collection Of GitHub Actions That Enable MLOps and CI/CD For Machine Learning:

Below is a collection of GitHub Actions that we are curating or building that facilitate machine learning workflows:

### 1. ChatOps
   - [Action: ChatOps From Pull Requests](https://github.com/marketplace/actions/chatops-for-pull-requests): Listens to ChatOps commands in PRs and emits variables that downstream Actions can branch on.


### 2. Submitting Argo workflows
[Argo](https://argoproj.github.io/) allows you to orchestrate machine learning pipelines that run on Kubernetes.

  - [Action: Submit Argo Workflows on GKE](https://github.com/marketplace/actions/submit-argo-workflows-to-gke) - leverages the gcloud CLI to authenticate to your GKE cluster and submit Argo Workflows.
  - [Action: Submit Argo Workflows on K8s (Cloud agnostic)](https://github.com/marketplace/actions/submit-argo-workflows-from-github) - requires that you supply a kubeconfig file to authenticate to your K8s cluster.

### 3. Query Experiment Tracking Results
  - [Action: Fetch runs from Weights & Biases](https://github.com/marketplace/actions/get-runs-from-weights-biases) - W&B is an experiment tracking and logging system for machine learning, and is free for open source projects.

### 4. Publish Docker Images
  - [Action: Publish Container To The GitHub Package Registry](https://github.com/marketplace/actions/publish-docker-images-to-gpr).  See this [doc](https://github.com/features/package-registry) on more information on the GitHub Package Registry.
  - [Action: Publish Container To a Generic Registry](https://github.com/marketplace/actions/publish-docker).
  
### 5. Compile and Push Pipeline to Kubeflow
- [Action: To compile, deploy and run Kubeflow pipeline](https://github.com/marketplace/actions/kubeflow-compile-deploy-and-run). This action allows you to instantiate [Kubeflow pipelines](https://www.kubeflow.org/docs/pipelines/overview/pipelines-overview/) from GitHub directly.

## What is MLOps?  

See [this demo](https://youtu.be/Ll50l3fsoYs) explaining this project and more background on what MLOps is and why it is needed.


## Example Of What We Are Trying To Solve With MLOps:

The code-review process re: Machine Learning often involves making decisions about merging or deploying code where critical information regarding model performance and statistics are not readily available.  This is due to the friction in including logging and statistics from model training runs in Pull Requests.  For example, consider this excerpt from a [real pull-request](https://github.com/kubeflow/code-intelligence/pull/54) concerning a machine learning project:

>![](images/pr.png)

In an ideal world, the participants in the above code review should be provided with all of the context necessary to evaluate the PR, including:

- Model performance metrics and statistics
- Comparison with baselines and other models on a holdout dataset
- Verification that the metrics and statistics correspond to the code changed in the PR, by tying the results to a commit SHA.
- Data versioning
- etc.

### How We Can Solve This With GitHub Actions:

[GitHub Actions](https://github.com/features/actions) allow you to compose a set of pre-built CI/CD tools or make your own, allowing you to compose a workflow that enables MLOps from GitHub.  The below example composes the following Actions into useful pipeline:

 [ChatOps](https://github.com/marketplace/actions/chatops-via-pr-labels) &rightarrow; [Deploy Argo ML Workflows](https://github.com/machine-learning-apps/gke-argo) &rightarrow;  [Weights & Biases Experiment Tracking](https://github.com/machine-learning-apps/wandb-action) -> Deploy Model:

>![](images/mlops.png)

View the demo pull request [here](https://github.com/machine-learning-apps/actions-ml-cicd/pull/34).  What is shown above is only the tip of the iceberg! 


## Explanation of Files In This Repo:

- **.github/workflows/**
   - **chatops.yaml**:  This workflow handles two different scenarios (1) when I want to execute a full model run with the command `/run-full-test` and (2) when I want to deploy a model using the ChatOps command `/deploy <run_id>`.  Note that you do not need to use ChatOps for your workflow, this was just the author's preferred way of triggering items.  You can use one of the many other [events that can trigger](https://help.github.com/en/actions/automating-your-workflow-with-github-actions/events-that-trigger-workflows) Actions.  Furthermore, these ChatOps commands uses a pre-defined action [machine-learning-apps/actions-chatops@master](https://github.com/marketplace/actions/chatops-for-pull-requests) that performs an Action by authenticating another GitHub app. The steps taken in this workflow trigger either the workflow defined in `ml-cicd.yaml` or `deploy.yaml`.
   - **ml-cicd.yaml**:  This workflow is triggered by the ChatOps command `/run-full-test` from events that occur in the `chatops.yaml` file. This executes the full training run of the model.
   - **deploy.yaml**: This workflow is triggered by the ChatOps command `/deploy <run_id>`. This workflow fetches the appropriate model artifacts associated with the `<run_id>` from the experiment tracking system (which is Weights & Biases in this case), and deploys this model using Google Cloud Functions.
   - **repo-dispatch.yaml**:  This workflow is triggered at the end of the Argo Workflow created in the step `Submit Argo Deployment` in `ml-cicd.yaml`.  [The terminal nodes](https://github.com/machine-learning-apps/actions-ml-cicd/blob/master/pipelines/workflow.yaml#L91-L162) of the Argo workflow creates a [repository dispatch](https://help.github.com/en/actions/automating-your-workflow-with-github-actions/events-that-trigger-workflows#external-events-repository_dispatch) event which triggers this workflow.  
   - **see-payload.yaml & see_token.yaml** - these files were used for debugging and can be safely ignored.  
- **/action_files**: these are a collection of shell scripts and python files that are run at various steps in the workflow files mentioned above.  
- **/src** - these are the files that define the pre-processing and training of the model.  These files are copied into the appropriate Docker container images in the workflow when the workflow is triggered.

## Recommended Way Of Getting Started With GitHub Actions and MLOps

The example in this repo is end-to-end and requires familiarity with Kubernetes and GitHub Actions to fully understand.  When starting out, we recommend automating one part of your workflow, such as deploying models.  As you learn more about the syntax of GitHub Actions you can increase the scope of your workflow as appropriate.  

We also encourage you to [make GitHub Actions for others to use](https://help.github.com/en/actions/automating-your-workflow-with-github-actions/publishing-actions-in-github-marketplace) to accommodate other tools. 

For any questions, please open an issue in this repo. 
