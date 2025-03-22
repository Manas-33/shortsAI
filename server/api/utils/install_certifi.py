# install_certifi.py
#
# Sample script to install or update a set of default Root Certificates
# for the ssl module. Uses the certificates provided by the certifi package:
# https://pypi.org/project/certifi/

import os
import os.path
import ssl
import stat
import subprocess
import sys

STAT_0o775 = (stat.S_IRUSR | stat.S_IWUSR | stat.S_IXUSR
              | stat.S_IRGRP | stat.S_IWGRP | stat.S_IXGRP
              | stat.S_IROTH | stat.S_IXOTH)


def main():
    openssl_dir, openssl_cafile = os.path.split(
        ssl.get_default_verify_paths().openssl_cafile)

    print(" -- pip install --upgrade certifi")
    subprocess.check_call([sys.executable,
                          "-E", "-s", "-m", "pip", "install", "--upgrade", "certifi"])

    import certifi

    # directory and target location
    print(f" -- removing any existing file at {openssl_cafile}")
    try:
        os.remove(openssl_cafile)
    except FileNotFoundError:
        pass

    # copy the file
    print(f" -- copying {certifi.where()} to {openssl_cafile}")
    with open(certifi.where(), 'rb') as certifi_file:
        with open(openssl_cafile, 'wb') as openssl_file:
            openssl_file.write(certifi_file.read())

    # permissions
    os.chmod(openssl_cafile, STAT_0o775)
    print(f" -- setting permissions on {openssl_cafile}")
    print(" -- update complete")


if __name__ == '__main__':
    main()
