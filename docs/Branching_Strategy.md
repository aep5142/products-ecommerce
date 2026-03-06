Git flow branching model:

1. **Main**: Branch from where the microservice will be running on its production environment. It's always alive. Can only be replicated for a *hotfix*.

2. **Develop**: Branch which will simulate the *main* branch. From this branch is where new features are born.

3. **Hotfix**: A replica from main only when a critical bug is detected and needs to be fixed fast. After it's fix, it will merge to main and Develop.

4. **Feature**: A replica from Develop. It's used to develop new features. When a new feature is ready, it merges into Develop and the branch dies.

5. **Release**: A replica from Develop. This branch simulates production environment, where if it succeeds it will be merged into Main (new version) and into Develop to have the latest changes.

