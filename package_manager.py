import settings
import requests
import cal
import os


class PackageManager:
    """This class download packages containing HikePrograms, HikeChains or ChainLoaders.
    """

    def pull(self, package_name):
        """
        Download a package in the appropriate directory
        """
        # if there is not a folder, download the package
        if not os.path.isdir(f"{settings.COMPONENTS_DIR}/{package_name}") and package_name != 'hike_default':
            url = f"{settings.PROGRAMS_REPOSITORY_URL}"
            r = requests.get(url, allow_redirects=True)
            data = r.json()['data']
            is_found = False
            for d in data:
                if d['name'] == package_name:
                    print(
                        f'Found {package_name} in the package list. Start cloning...')
                    print(d)
                    is_found = True
                    cal.clone_repo(
                        d['git_url'], f"{settings.COMPONENTS_DIR}/{package_name}", d['tag'])

            if not is_found:
                raise Exception(
                    f"package {package_name} not found in the repository")
        return True
