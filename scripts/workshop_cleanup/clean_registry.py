from __future__ import print_function
import argparse
import json
import sys
import urllib
import urllib2


class Result(object):
    '''
    Represents a successful or failed operation and some metadata about it.
    '''
    def __init__(self, is_success=True, message=None):
        self.is_success = is_success
        self.message = message


class Report(object):
    '''
    Represents the overall results of the program.

    How many tags did we find to delete, how many did we successfully delete and
    information about any failures we had.
    '''
    def __init__(self, to_be_deleted):
        self.to_be_deleted = to_be_deleted
        self.successes = 0
        self.failure_messages = []

    @property
    def failures(self):
        return len(self.failure_messages)

    def inc_success(self):
        self.successes += 1

    def add_failure(self, msg):
        self.failure_messages.append(msg)


def api_url():
    return 'https://registry.ford.com/api/v1'


def current_tag(tag_body):
    '''
    The tags list holds a record of tags that are no longer used. These tags
    will have an `end_ts` field indicating when they were removed.
    '''
    return tag_body.get("end_ts") is None


def extract_tag_names(tag_bodies):
    '''
    Pulls the names out of any tag bodies that are still considered current.

    Each body will have a structure like this:
    ```json
    {
            "name": "gcline5",
            "reversion": false,
            "end_ts": 1581360227,
            "start_ts": 1581357029,
            "docker_image_id": "1579844b36083ac629f97787a17a07db47666c1095d6cbeb0fbe80df3b1cad26",
            "manifest_digest": "sha256:dd09337cd7531a5b484615302528be5ec95d47b9ca895737910aec177e7ecbca"
    }
    ```
    `end_ts` might be missing if the tag is still used.
    '''
    for tag_body in tag_bodies:
        if current_tag(tag_body) and tag_body.get("name"):
            yield tag_body["name"]


def get_tag_page(repo, token, page=1, limit=100):
    '''
    Makes a single request to get tags from the repo with a given page offset.

    Each page will have a structure as follows:
    ```json
    {
        "has_additional": true/false,
        "page": 1,
        "tags": [
            tag_bodies...
        ]
    }
    ```
    '''
    params = urllib.urlencode({'page': page, 'limit': limit})
    tag_url = '{api}/repository/{repo}/tag/?{params}'.format(
        api=api_url(),
        repo=repo,
        params=params,
    )
    request = urllib2.Request(
        tag_url,
        headers={'Authorization': 'Bearer {token}'.format(token=token)},
    )
    f = urllib2.urlopen(request)
    body = f.read()
    parsed = json.loads(body)
    f.close()

    return parsed


def get_all_tag_pages(repo, token):
    '''
    Repeatedly calls the Quay API and yields each result so we can lazily process
    each set of results. Each yielded value will be a list of tag bodies.
    '''
    page = get_tag_page(repo, token)
    yield page.get('tags', [])
    while page.get('has_additional'):
        page_num = page.get('page', 1)
        page = get_tag_page(repo, token, page=page_num + 1)

        yield page.get('tags', [])


def find_tags(repo, token):
    '''
    Gets the names of all still current tags used in the repo.

    This will return a list like:
    ```python
    ['tag_1', 'tag_2', 'tag_3']
    ```
    '''
    tag_names = [
        tag_name
        for tag_page in get_all_tag_pages(repo, token)
        for tag_name in extract_tag_names(tag_page)
    ]

    return tag_names


def delete_tag(repo, token, tag):
    '''
    Attempts to delete a given tag. If successful it will return a successful
    Result, otherwise it will record some information about why the attempt failed
    and return that information.
    '''
    delete_url = '{api}/repository/{repo}/tag/{tag}'.format(
        api=api_url(),
        repo=repo,
        tag=tag,
    )
    request = urllib2.Request(
        delete_url,
        headers={'Authorization': 'Bearer {token}'.format(token=token)}
    )

    # This is a weird work around. There's no argument for method so we redefine
    # the `get_method` method on the object.
    request.get_method = lambda: 'DELETE'
    try:
        urllib2.urlopen(request)
    except Exception as e:
        return Result(
            False,
            {
                'tag': tag,
                'error': str(e),
                'msg': 'Error while deleting the tag',
            }
        )

    return Result(True)


def delete_tags(repo, token, tags):
    '''
    Deletes all the tags given and compiles a report of the results.
    '''
    report = Report(len(tags))
    for tag in tags:
        result = delete_tag(repo, token, tag)
        if result.is_success:
            report.inc_success()
        else:
            report.add_failure(result.message)

    return report


def main():
    parser = argparse.ArgumentParser(description='Clear all tags from a Quay repo')
    parser.add_argument(
        'repo',
        type=str,
        help='The URL of the repo e.g. devenablement/workshop',
    )
    parser.add_argument(
        'token',
        type=str,
        help='The API token for the repository. It must have read/write permissions.',
    )
    parser.add_argument(
        '--verbose', '-v',
        action='store_true',
        help='Prints extra information on failures',
    )

    args = parser.parse_args()

    tags = find_tags(args.repo, args.token)
    report = delete_tags(args.repo, args.token, tags)

    print(
        '''Total Tags: {total_count}
Successfully deleted: {deleted_count}
Failed: {failed_count}'''.format(
            total_count=report.to_be_deleted,
            deleted_count=report.successes,
            failed_count=report.failures,
        ))
    if args.verbose:
        print(json.dumps(report.failure_messages, indent=2))

    if report.failures > 0:
        sys.exit(1)


if __name__ == '__main__':
    main()

