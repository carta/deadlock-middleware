# deadlock-middleware
A middleware to automatically retry requests in the case of a deadlock.

## Development

### Install dependencies

All dependencies

```
pip install -r requirements/dev.txt
```

Only production dependencies

```
pip install -r requirements/release.txt
```

### Lint

```
make lint
```

### Test

```
make test
```

### Format

```
make black # checks formatting
make fix-black # fixes formatting
```

### Typecheck

```
make typecheck
```

### Sorted Import

```
make sort # checks import sorting
make fix-sort # fixes import sorting
```

### Deployment


- [ ] Modify the [terraform-github](https://github.com/carta/terraform-github) repo to add a new repository for your package
- [ ] Tag @sre on #platform-engineering and make sure they add your new repo as a project on CircleCI
- [ ] Make sure to get the SRE team to add the **Python Cloudsmith API key** to your CircleCI project to make your package available to other developers. 
