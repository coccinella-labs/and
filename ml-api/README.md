# ml-api  
build, deploy, and scale machine learning with ease.

![ML API](images/ml-api.png)

## features  
- **upload models**: deploy your models effortlessly.  
- **real-time inference**: generate predictions instantly.  
- **version management**: keep your models organized and up to date.  

## get started  
1. clone the repository:  
   ```bash  
   git clone https://github.com/coccinella-labs/and.git  
   ```

2. navigate to the project:

   ```bash
   cd ml-api  
   ```
3. install dependencies:

    ```bash
    pip install -r requirements.txt  
    ```

    Note: numpy is not included in requirements.txt due to Python version constraints. For local development with numpy 2.3.3, ensure Python >=3.14 and install separately: `pip install numpy==2.3.3`. Docker builds use Python 3.14 and install numpy 2.3.3 automatically.

## deploy the web interface

```bash
kubectl apply -f k8s.yaml
```

## run the api

launch the server with:

```bash
python main.py  
```

### example request

```bash
curl -X POST http://localhost:8000/chat -H "Content-Type: application/json" -d '{"prompt": "Hello, world!"}'
```

### additional endpoints

- `GET /models`: list available models
- `GET /status`: get api and model status

## requirements

* python 3.14+
* fastapi, huggingface transformers, pytorch 2.9.1, numpy (see installation notes)

## local-first platform

You can run the entire stack locally without external hosting. The control plane builds and deploys the `ml-api` container into a local Docker runtime and exposes a management API on port `9000`.

1. From the workspace root (the parent directory that contains both `ml-api/` and `local_platform/`), install Python dependencies for both services:

   ```bash
   pip install -r ml-api/requirements.txt -r local_platform/requirements.txt
   ```

2. Ensure Docker is running, then start the control plane:

   ```bash
   cd local_platform
   uvicorn control_plane:app --reload --port 9000
   ```

3. Trigger a build and deployment of `ml-api`:

   ```bash
   curl -X POST http://localhost:9000/deploy -H "Content-Type: application/json" -d '{}'
   ```

   The control plane builds the `ml-api` image via the included Dockerfile, runs the container on `http://localhost:8080`, and exposes status via `/apps` or `/status`.

4. When deployment finishes, your hosted ml-api is available at `http://localhost:8080/chat`. Use the API endpoints from that URL and monitor the control plane via `http://localhost:9000/status`.

5. Optionally push the image into a local registry once you're satisfied:

   ```bash
   curl -X POST http://localhost:9000/deploy -H "Content-Type: application/json" -d '{"push_to_registry": true, "registry": "localhost:5000"}'
   ```

This setup mirrors a full hosting pipeline while keeping everything on your machine, so you can experiment with builds, deployments, and networking without needing cloud credits.

## workspace layout

The repository assumes `ml-api/` and `local_platform/` stay side-by-side. The stack depends on those local paths, so we document that rationale in `WORKSPACE_LAYOUT.md`.

## contribute

shape the future of ml-api. submit issues or pull requests to make it even better.

## conventional commits

this project follows conventional commit standards to ensure clear and consistent commit messages.

### setup

to enable commit message validation:

1. copy the hook script to your local git hooks:

   for unix/linux/macos:
   ```bash
   cp scripts/commit-msg .git/hooks/commit-msg
   chmod +x .git/hooks/commit-msg
   ```

   for windows (powershell):
   ```powershell
   cp scripts/commit-msg.ps1 .git/hooks/commit-msg
   ```

### commit message format

commit messages must follow this format:

* start with a type: `feat:`, `fix:`, `docs:`, `style:`, `refactor:`, `test:`, `chore:`, `perf:`, `ci:`, `build:`, `revert:`
* followed by a space and a lowercase description
* first line ≤60 characters

example: `feat: add user authentication`

### history cleanup

if you need to clean up existing commit messages (make lowercase and truncate), use the rewrite script:

for unix/linux/macos:
```bash
bash scripts/rewrite_msg.sh
```

for windows (powershell):
```powershell
get-content | scripts/rewrite_msg.ps1
```

for rewriting the entire history:

```bash
git filter-branch --msg-filter 'bash scripts/rewrite_msg.sh' -- --all
```

(on windows, use powershell equivalent)

note: this rewrites history, so use with caution and force-push if necessary.

## releases

to create an alpha release:

```bash
bash scripts/release_alpha.sh
```

this will bump the version, create a tag, push, and publish a prerelease on github.

## license

licensed under the mit license. see the [LICENSE](LICENSE) file for details.
