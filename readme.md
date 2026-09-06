<p align="center">
  <img src="https://raw.githubusercontent.com/Coccinella-Labs/and/main/.github/assets/thumbnail.png" alt="and" width="100%">
</p>

# [...]

# Builds `ml-api` using `ml-api/Dockerfile`
# Expects model code, dependencies, Dockerfile, and fine-tuned assets to live under `ml-api/`
# References `ml-api` via relative paths (for example, in `local_platform/builder.py`)

Removing the directory and keeping only a Git URL would require adding cloning and synchronization logic before every build. By keeping `ml-api` in the repository, the control plane can:

# Operate offline
# Rebuild quickly without extra setup
# Version infrastructure, model code, and assets together

To update `ml-api`, simply pull upstream changes into the `ml-api/` directory and re-run the deployment.

**Learn more:** see the control plane build flow and path assumptions in `local_platform/builder.py`.

## Extending this workspace

If you decide to extend the local-first stack, feel free to reach out before making structural changes; we can coordinate so both `ml-api/` and `local_platform/` continue to work together. The control plane expects the artifacts listed above, so keep those paths intact when you test new builds or add services.
