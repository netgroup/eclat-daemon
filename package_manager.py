import settings
import requests
import cal
import os
import logging

logger = logging.getLogger()

class PackageManager:
    """
    Download packages containing HikePrograms, HikeChains or ChainLoaders from
    the central repository.
    """

    def pull(self, package_name):
        """
        Download a package in the appropriate directory.
        Return True if downloaded, false if already exists, and throw exception in case of errors.
        """
        # if is a system package or if the package has been already downloaded, do nothing.
        if package_name == 'hike_default' or os.path.isdir(f"{settings.COMPONENTS_DIR}/{package_name}"):
            return False


        url = f"{settings.PROGRAMS_REPOSITORY_URL}"
        r = requests.get(url, allow_redirects=True)
        data = r.json()['data']
        is_found = False
        for d in data:
            if d['name'] == package_name:
                logger.info(
                    f'Found {package_name} in the package list. Start cloning...')
                logger.info(f"Package information retrieved: {str(d)}")
                is_found = True
                cal.clone_repo(
                    d['git_url'], f"{settings.COMPONENTS_DIR}/{package_name}", d['tag'])
                logger.info(f"Package {package_name} cloned successfully")

        if not is_found:
            raise Exception(
                f"package {package_name} not found in the repository")
        
        return True
