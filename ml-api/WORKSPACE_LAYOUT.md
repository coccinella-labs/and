## Repository layout rationale

`ml-api` is kept in-tree (as a sibling to `local_platform`) because the control plane
builds from local paths, assumes offline operation, and versions model code and
infrastructure together. Replacing it with a Git URL would require cloning and sync
logic on every build.