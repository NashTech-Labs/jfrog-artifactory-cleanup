#!/usr/bin/python
"""
Clean Up Docker Artifacts which not used for given weeks
"""
from __future__ import print_function

import requests
import argparse
import textwrap
import os
import sys

__author__ = "Kumar Pratik"
__version__= "1.0"


example = textwrap.dedent("""
Examples:
* Dry run for cleaning up artifacts not downloaded for x weeks. Default weeks to scan is 52w
cleanup_docker_artifacts.py clean --url $ARTIFACTORY_URL --repo $REPO_NAME --path sfrm -U $ARTIFACTORY_USER -P $API_KEY --before_weeks 30w
*  cleaning up cleaning up artifacts not downloaded for x weeks. Default weeks to scan is 52w
cleanup_docker_artifacts.py clean --url $ARTIFACTORY_URL --repo $REPO_NAME --path sfrm -U $ARTIFACTORY_USER -P $API_KEY --before_weeks 30w -d
* To show artifacts not downloaded for x weeks.  Default weeks to scan is 52w
cleanup_docker_artifacts.py show --url $ARTIFACTORY_URL --repo $REPO_NAME --path sfrm -U $ARTIFACTORY_USER -P $API_KEY --before_weeks 30w 
* Scan artifacts for Top Level REPO without REPO PATH. Default weeks to scan is 52w
cleanup_docker_artifacts.py show --url $ARTIFACTORY_URL --repo $REPO_NAME -U $ARTIFACTORY_USER -P $API_KEY --before_weeks 30w
""").format(os.path.basename(sys.argv[0]))
formatter_class = argparse.RawDescriptionHelpFormatter
parser = argparse.ArgumentParser(description="CLI Tool helps to show and clean artifacts in Artifactory, \
     can analyse the repository artifacts not downloaded for given number of weeks and delete them", epilog=example,formatter_class=formatter_class)
 

subparsers = parser.add_subparsers(help='Specify clean or show as sub command', dest='command')

clean_parser = subparsers.add_parser('clean', help='To clean artifactory artifacts not downloaded x no of weeks. Works Best for Docker based repos')
clean_parser.add_argument('--url', '-u', dest='artifactory_url', type=str, help="Artifactory URL", required=True)
clean_parser.add_argument('--repo', '-r', dest='artifactory_repo', type=str, help="Artifactory Repository Name", required=True)
clean_parser.add_argument('--path', '-p', dest='artifactory_repo_path', type=str, default="", help="Artifactory Repository Name")
clean_parser.add_argument('--artifactory_user', '-U', dest='artifactory_user', type=str, help="Artifactory Username", required=True)
clean_parser.add_argument('--apikey', '-P',dest='artifactory_api_key', type=str, help="Artifactory User API KEY", required=True  )
clean_parser.add_argument('--before_weeks',dest='before_weeks_to_delete', type=str, default= "52w", help="This script delete artifactory not downloaded for given no of weeks")
clean_parser.add_argument('--delete','-d', dest='delete',action='store_true', default=False, help="By dafault dry run is True, if you want to override dry run please add --dryrun False this accepts only bool value")

show_parser = subparsers.add_parser('show', help='To Show Disk Memory details artifactory repositories given in sub command')
show_parser.add_argument('--url', '-u', dest='artifactory_url', type=str, help="Artifactory URL", required=True)
show_parser.add_argument('--repo', '-r', dest='artifactory_repo', type=str, help="Artifactory Repository Name", required=True)
show_parser.add_argument('--path', '-p', dest='artifactory_repo_path', type=str, default="", help="Artifactory Repository Name")
show_parser.add_argument('--artifactory_user', '-U', dest='artifactory_user', type=str, help="Artifactory Username", required=True)
show_parser.add_argument('--apikey', '-P',dest='artifactory_api_key', type=str, help="Artifactory User API KEY", required=True)
show_parser.add_argument('--before_weeks',dest='before_weeks_to_delete', type=str, default= "52w", help="This script delete artifactory not downloaded for given no of weeks")

args = parser.parse_args()

def clean_docker():
    """
    Function used to clean up docker images in artifactory
    """
    base_url = args.artifactory_url;

    headers = {
        'content-type': 'text/plain',
    }

    timeline = args.before_weeks_to_delete

    data = 'items.find({"name":{"$eq":"manifest.json"},"type":"file","stat.downloaded":{"$before":"'+timeline+'"},"repo":"'+args.artifactory_repo+'" , "path":{"$match":"'+args.artifactory_repo_path+'*"} }).include("name", "repo", "path", "size", "stat.downloaded")'

    _allowed_delete = args.delete
   
    myResp = requests.post(base_url+'/api/search/aql', auth=(args.artifactory_user, args.artifactory_api_key), headers=headers, data=data)

    for result in eval(myResp.text)["results"]:
        artifact_url = base_url+ '/' + result['repo'] + '/' + result['path']
        
        if _allowed_delete:
            requests.delete(artifact_url, auth=(args.artifactory_user, args.artifactory_api_key))  # This will delete files. 
            print(artifact_url+"  __DELETED")
        else:
            print(artifact_url+"  WILL_BE__DELETED_WITH_DRY_RUN_FALSE")

def show_size():
    """
    Function used to show size of repo and paths in artifactory
    """
    base_url = args.artifactory_url;
    headers = {
        'content-type': 'text/plain',
    }
    timeline = args.before_weeks_to_delete
    data = 'items.find({"name":{"$eq":"manifest.json"},"type":"file","stat.downloaded":{"$before":"'+timeline+'"},"repo":"'+args.artifactory_repo+'" , "path":{"$match":"'+args.artifactory_repo_path+'*"} }).include("name", "repo", "path", "size", "stat.downloaded")'
    myResp = requests.post(base_url+'/api/search/aql', auth=(args.artifactory_user, args.artifactory_api_key), headers=headers, data=data)
    print(myResp.text)
    
if __name__ == '__main__':
    if args.command == 'clean':
        clean_docker()
    if args.command == 'show':
        show_size()