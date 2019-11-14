"""
Models for datafile lookup / verification.
"""


class LookupStatus():
    """
    Enumerated data type for lookup states.
    """
    NOT_STARTED = 0

    IN_PROGRESS = 1

    # Not found on MyTardis, need to upload this file:
    NOT_FOUND = 2

    # Found on MyTardis (and verified), no need to upload this file:
    FOUND_VERIFIED = 3

    # Found unverified DataFile record, but we're using POST, not staged
    # uploads, so we can't retry without triggering a Duplicate Key error:
    FOUND_UNVERIFIED_UNSTAGED = 4

    # Finished uploading to staging, waiting
    # for MyTardis to verify (don't re-upload):
    FOUND_UNVERIFIED_FULL_SIZE = 5

    # Partially uploaded to staging, need to resume upload or re-upload:
    FOUND_UNVERIFIED_NOT_FULL_SIZE = 6

    # Missing datafile objects (replicas) on server:
    FOUND_UNVERIFIED_NO_DFOS = 7

    # An unverified DFO (replica) was created previously, but the file
    # can't be found on the staging server:
    NOT_FOUND_ON_STAGING = 8

    # Verification failed, should upload file, unless the failure
    # was so serious (e.g. no network) that we need to abort everything.
    FAILED = 9


class Lookup():
    """
    Model for datafile verification / lookup.
    """
    def __init__(self, folder, datafile_index):
        self.folder_name = folder.name
        self.subdirectory = folder.get_datafile_directory(datafile_index)
        self.datafile_index = datafile_index
        self.filename = folder.get_datafile_name(datafile_index)
        self.message = ""
        self.status = LookupStatus.NOT_STARTED
        self.complete = False

        # If during verification, it has been determined that an
        # unverified DataFile exists on the server for this file,
        # its DataFileModel object will be recorded:
        self.existing_unverified_datafile = None
