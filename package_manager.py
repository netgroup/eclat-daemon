import settings
import requests
import cal
import os
import logging

logger = logging.getLogger(__name__)

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
        # if there is not a folder, download the package
        if package_name == 'hike_default':
            raise Exception("Attempt to fetch the hike_default package. This is a system package which is already installed.")

        if os.path.isdir(f"{settings.COMPONENTS_DIR}/{package_name}"):
            logger.info(f"Attempting to download package '{package_name}' which is already downloaded")
            return False


        url = f"{settings.PROGRAMS_REPOSITORY_URL}"
        r = requests.get(url, allow_redirects=True)
        data = r.json()['data']
        is_found = False
        for d in data:
            if d['name'] == package_name:
                logger.info(
                    f'Found {package_name} in the package list. Start cloning...')
                logger.info(d)
                is_found = True
                cal.clone_repo(
                    d['git_url'], f"{settings.COMPONENTS_DIR}/{package_name}", d['tag'])

        if not is_found:
            raise Exception(
                f"package {package_name} not found in the repository")
        
        return True
