import pathlib
import zipfile
import logging
from urllib.request import urlretrieve
logger = logging.getLogger(__name__)


class BaseTractDownloader(object):
    THIS_DIR = pathlib.Path(__file__).parent

    def __init__(self):
        self.data_dir = self.THIS_DIR.joinpath("data", "tracts")
        if not self.data_dir.exists():
            self.data_dir.mkdir()

    def run(self):
        self.download()
        self.unzip()

    def download(self):
        """
        Downloads the TIGER SHP file of Census block for the provided state and county.
        Returns the path to the ZIP file.
        """
        # Check if the zip file already exists
        zip_path = self.data_dir.joinpath(self.zip_name)
        if zip_path.exists():
            logger.debug(f"ZIP file already exists at {zip_path}")
            return zip_path

        # If it doesn't, download it from the Census FTP
        logger.debug(f"Downloading {self.url} to {zip_path}")
        urlretrieve(self.url, zip_path)

        # Return the path
        return zip_path

    def unzip(self):
        """
        Unzip the provided ZIP file.
        """
        shp_path = pathlib.Path(self.zip_name.replace(".zip", ".shp"))
        if shp_path.exists():
            logger.debug(f"SHP already unzipped at {shp_path}")
            return shp_path

        zip_path = self.data_dir.joinpath(self.zip_name)
        logger.debug(f"Unzipping {zip_path} to {self.data_dir}")
        with zipfile.ZipFile(zip_path, "r") as z:
            z.extractall(self.data_dir)
        return shp_path


class TractDownloader2010(BaseTractDownloader):
    zip_name = "tl_2010_06_tract10.zip"
    url = f"https://www2.census.gov/geo/tiger/TIGER2010/TRACT/2010/{zip_name}"


class TractDownloader2000(BaseTractDownloader):
    zip_name = "tl_2009_06_tract00.zip"
    url = f"https://www2.census.gov/geo/tiger/TIGER2009/06_CALIFORNIA/{zip_name}"
