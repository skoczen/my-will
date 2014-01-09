import yaml
from github3 import login
from will import settings
from will.utils import Bunch

class GithubMixin(object):
    def refresh_all_cached_github_info(self):
        self.get_github_deployable_repos(force_load=True)
        self.get_github_all_repos(force_load=True)
        return True

    def get_github_api(self, force_load=False):
        if force_load or not hasattr(self, "_github_api"):
            self._github_api = login(settings.WILL_GITHUB_USERNAME, password=settings.WILL_GITHUB_PASSWORD)
        return self._github_api

    def get_github_org(self, org_name=None, force_load=False):
        if not org_name:
            org_name = settings.WILL_GITHUB_ORGANIZATION_NAME
        if force_load or not hasattr(self, "_github_org"):
            self._github_org = self.get_github_api(force_load=force_load).organization(org_name)
        return self._github_org

    def get_github_repos(self, force_load=False):
        return self.get_github_org(force_load=force_load).iter_repos()

    def get_github_branches(self, only_deployable=False):
        repos = []
        for repo in self.get_github_repos():
            if not repo.fork:
                branches = []
                for b in repo.iter_branches():
                    deployable = False
                    deploy_config = None
                    if only_deployable:
                        deploy_config = repo.contents("deploy.yml", ref=b.commit.sha)
                        if deploy_config:
                            deploy_config = yaml.load(deploy_config.content.decode("base64"))
                            deployable = True
                    if not only_deployable or deployable:
                        branches.append(Bunch(
                            url="%s/tree/%s" % (repo.html_url, b.name),
                            repo_name=repo.name,
                            repo_obj=repo,
                            repo_clone_url=repo.ssh_url,
                            name=b.name,
                            branch_obj=b,
                            deployable=deployable,
                            deploy_config=deploy_config,  # Note this will only be set for deployable branches.
                        ))
                if len(branches) > 0:
                    repos.append(Bunch(
                        name=repo.name, 
                        branches=branches, 
                        url=repo.html_url,
                        clone_url=repo.clone_url,
                    ))
        return repos

    def get_github_deployable_repos(self, force_load=False):
        deployable_branches = self.load("will_github_deployable_branches", False)
        if not deployable_branches or force_load:
            self._github_deployable_branches = self.get_github_branches(only_deployable=True)
            self.save("will_github_deployable_branches", self._github_deployable_branches)
        else:
            self._github_deployable_branches = deployable_branches
        return self._github_deployable_branches        

    def get_github_all_repos(self, force_load=False):
        all_branches = self.load("will_github_all_branches", False)
        if not all_branches or force_load:
            self._github_all_branches = self.get_github_branches()
            self.save("will_github_all_branches", self._github_all_branches)
        else:
            self._github_all_branches = all_branches
        return self._github_all_branches

    def get_branch_from_branch_name(self, branch_name, is_deployable=False):
        matches = []
        if is_deployable:
            all_repos = self.get_github_deployable_repos()
        else:
            all_repos = self.get_github_all_repos()

        for r in all_repos:
            for b in r.branches:
                if (b.name == branch_name or 
                    b.name == "feature/%s" % (branch_name,) or
                    "%s/%s" % (b.repo_name, b.name) == branch_name or
                    "%s/feature/%s" % (b.repo_name, b.name) == branch_name or
                    "%s:%s" % (b.repo_name, b.name) == branch_name or
                    "%s:feature/%s" % (b.repo_name, b.name) == branch_name
                   ):
                    matches.append(b)
        if len(matches) == 0:
            return None
        elif len(matches) == 1:
            return matches[0]

        return matches
