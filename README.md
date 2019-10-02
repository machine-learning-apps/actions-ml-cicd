## Resources For Machine Learning CI/CD With GitHub Actions

Read [this article](https://blog.paperspace.com/ci-cd-for-machine-learning-ai/) for a primer on what CI/CD for Machine Learning is and how it differs from traditional CI/CD .

## GitHub Actions That Enable CI/CD For Machine Learning

### 1. ChatOps
   - [Action: ChatOps From Pull Requests](https://github.com/marketplace/actions/chatops-for-actions): Listens to ChatOps commands in PRs and emits variables that downstream Actions can branch on.

### 2. Submitting Argo workflows
[Argo](https://argoproj.github.io/) allows you to orechestrate machine learning pipelines that run on Kubernetes.

  - [Action: Submit Argo Workflows on GKE](https://github.com/marketplace/actions/submit-argo-workflows-to-gke) - leverages the gcloud cli to authenticate to your GKE cluster and submit argo workflows.
  - [Action: Submit Argo Workflows on K8s (Cloud agnostic)](https://github.com/marketplace/actions/submit-argo-workflows-from-github) - requires that you supply a kubeconfig file to authenticate to your k8 cluster.

### 3. Query Experiment Tracking Results
  - [Action: Fetch runs from Weights & Biases](https://github.com/marketplace/actions/get-runs-from-weights-biases) - W&B is an experiment tracking and logging system for machine learning, and is free for open source projects.

### 4. Publish Docker Images
  - [Action: Publish Container To The GitHub Package Registry](https://github.com/marketplace/actions/publish-docker-images-to-gpr).  See this [doc](https://github.com/features/package-registry) on more information on the GitHub Package Registry
  - [Action: Publish Container To a Generic Registry](https://github.com/marketplace/actions/publish-docker)


## Demonstrations of ML CI/CD

 - TODO2
