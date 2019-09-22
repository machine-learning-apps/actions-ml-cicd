## Resources For Machine Learning CI/CD With GitHub Actions

Read [this article](https://blog.paperspace.com/ci-cd-for-machine-learning-ai/) for a primer on what CI/CD for Machine Learning is and how it differs from traditional CI/CD .

## GitHub Actions That Enable CI/CD For Machine Learning

- **Submitting [Argo workflows](https://argoproj.github.io/)** - kick off machine learning pipelines that run on Kubernetes from GitHub:
  - [On GKE](https://github.com/marketplace/actions/submit-argo-workflows-to-gke) - leverages the gcloud cli to authenticate to your GKE cluster and submit argo workflows.
  - [Cloud agnostic](https://github.com/marketplace/actions/submit-argo-workflows-from-github) - requires that you supply a kubeconfig file to authenticate to your k8 cluster.

- **Query Experiment Tracking Results**
  - Fetch runs [from Weights & Biases](https://github.com/machine-learning-apps/wandb-action)

- **Publish Docker Images**
  - [To the GitHub Package Registry](https://github.com/marketplace/actions/publish-docker-images-to-gpr)
  - [To a generic registry](https://github.com/marketplace/actions/publish-docker)


### Demonstrations of ML CI/CD

TODO
