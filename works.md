# Repository Updates and Actions  

## Migration to `setup.cfg` and `pyproject.toml` (#57)  
### Description  
With the release of `pip 24.2+`, the `pip install -e .` command returns a deprecation warning for legacy editable installs. Future versions (`pip 25.0`) will enforce these changes.  

To address this:  
- Migrated the repository to use a modern `pyproject.toml` and `setup.cfg` setup.  
- Incorporated a workflow to update `setup.cfg` automatically when `codemeta.json` changes, via the `codemeta2cff.yml` GitHub Action.  

### Pending Items  
- Explore methods to pull metadata from `codemeta.json` for automation.  
- Add compatibility for `editable_mode=compat` to ensure seamless installs.  

---

## Run Tests with GitHub Actions (#46)  
### Description  
Created and integrated a GitHub Action to automate repository testing and validation:  
- Added token as an environment variable to validate the publisher field in `cli.py`.  
- Action is designed to:  
  - Fail for pull requests anything that makes `cli.py` not run or fail.  
  - Pass for pull requests that only modify `README.md`.  


---

## Miscellaneous Improvements  
- Replaced outdated `datacite43` files with files from the current version of `CaltechDATA`.  
- Integrated a script to fetch metadata via `caltechdata_api`.  

### Contributions  
- Developed a GitHub Action to sync changes in `setup.py` with updates to `codemeta.json`.  

### Activity Highlights  
- Issues and tasks assigned to @RohanBhattaraiNP.  
- Progress reviewed and comments provided by @tmorrell.  

---

For any questions or contributions, please feel free to open a discussion or pull request!  
