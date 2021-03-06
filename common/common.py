from jbosscli import Jbosscli, Deployment

import os


def initialize_controller(args):
    """Try to instantiate and return the controller object.
    In case of errors, print it and return None.
    """
    try:
        return Jbosscli(args.controller, args.auth)
    except Exception as e:
        print e
        return None


def fetch_enabled_deployments(controller, archives=[]):
    """Fetch a list of enabled deployments with the same runtime name as
    the archives to deploy.

    Arguments:
    controller -- the controller to fetch the deployments from
    archives   -- the archives to be deployed

    This function updates the archives with fresh information from the
    controller, such as the server group and if it is enabled or not.

    It is mainly used to provide information to the undeploy script generation.
    """
    deployments = get_assigned_deployments(controller)

    if not archives:
        return [x for x in deployments if x.enabled]

    runtime_names = {}
    for archive in archives:
        runtime_names[archive.runtime_name] = archive

    enabled_deployments = []
    for deployment in deployments:
        if deployment.runtime_name in runtime_names and deployment.enabled:
            enabled_deployments.append(deployment)
            runtime_names[deployment.runtime_name].enabled = True
            runtime_names[deployment.runtime_name].server_group = \
                deployment.server_group

    return enabled_deployments

def get_assigned_deployments(controller):
    deployments = []
    if controller.domain:
        map(
            lambda d: deployments.extend(d),
            [group.deployments for group in controller.server_groups]
        )
    else:
        deployments = controller.deployments

    return deployments


def write_to_file(file, content):  # pragma: no cover
    """Write content to file."""
    with open(file, "w") as f:
        f.write(content)


def read_from_file(path):  # pragma: no cover
    lines = []
    with open(path) as f:
        lines = f.readlines()

    return lines


def is_archive(file):
    """Return true if file name ends with .ear, .war or .jar"""
    return file.endswith('.ear') or \
        file.endswith('.war') or \
        file.endswith('.jar')


def read_archive_files(path, tag, files=[]):
    """Scan path looking for archive files. Return a list of archives
    with tag applied to their names. runtime_name remains as the filename.
    """
    archives = []

    for file in os.listdir(path):
        runtime_name = file.split(os.sep)[-1]
        if (not files or runtime_name in files) and is_archive(file):
            name = runtime_name.replace(".ear", "")\
                .replace(".war", "")\
                .replace(".jar", "") + "-" + tag

            deployment = Deployment({
                "name": name,
                "runtime-name": runtime_name,
                "enabled": False
            }, None)

            archives.append(deployment)

    return archives


def extract_tag(path):
    """Extract the name of the directory where the deployments are placed.

    Arguments:
    path -- the path to extract the name from.

    This simply reads the leaf dir in a path.
    "/path/to/deployment" returns "deployment"
    "../relative/path/" returns "path"
    "abc" returns "abc"
    """

    if path.endswith(os.sep):
        path = path[:-1]

    return path.split(os.sep)[-1]


def generate_rollback_filename_template(rollback_info_file_suffix):
    if not rollback_info_file_suffix:
        return "rollback-info_"
    else:
        return "rollback-info-{0}_".format(rollback_info_file_suffix)
