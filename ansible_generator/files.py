# -*- coding: utf-8 -*-
u"""files is used to generate the necessary file."""
from ansible_generator.log import setup_logger
from ansible_generator.utilities import join_cwd_and_directory_path

# python stdlib
from os import utime
from logging import INFO


def create_file_layout(projects=None,
                       inventories=[u'production', u'staging'],
                       alternate_layout=False,
                       verbosity=INFO):
    logger = setup_logger(name=__name__, log_level=verbosity)
    minimum_paths = [u'site.yml']
    if alternate_layout:
        required_paths = get_alternate_inventories_file_paths(
            logger=logger, inventories=inventories) + minimum_paths
    else:
        required_paths = minimum_paths + inventories

    logger.debug('msg="{n} required files" files="{p}"'.format(
        n=len(required_paths), p=required_paths))

    if projects:
        logger.debug(
            'msg="projects was defined" projects="{p}"'.format(p=projects))

        final_paths = []
        for project in projects:
            final_paths += [
                u'{project}/{path}'.format(project=project, path=required_path)
                for required_path in required_paths
            ]
        required_paths = final_paths
        logger.debug('msg="{n} project required files" files="{p}"'.format(
            n=len(required_paths), p=required_paths))
    required_paths = map(join_cwd_and_directory_path, required_paths)

    for required_path in required_paths:
        success = touch(logger=logger, filename=required_path)
        if not success:
            return False
    return True


def get_alternate_inventories_file_paths(logger, inventories):
    logger.debug(u'building alternate inventory layout file paths')
    inventory_paths = []
    for inventory in inventories:
        inventory_paths.append(
            u'inventories/{inventory}/hosts'.format(inventory=inventory))
    return inventory_paths


def touch(logger, filename, times=None):
    try:
        logger.info('creating file {filename}'.format(filename=filename))
        with open(filename, 'a') as f:
            try:
                utime(filename, times)
            finally:
                f.close()
        return True
    except Exception:
        logger.error('failed to create file', exc_info=True)
        return False