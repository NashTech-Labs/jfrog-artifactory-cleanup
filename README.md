# Artifactory Clean Up 

This Scripts cleans all the image older than a given period in jfrog artifactory. 


## Run CLI in local 


````
knoldus@knoldus-Latitude-3510:~$ ./artifactory_cleanup.py --help
usage: artifactory_cleanup.py [-h] {clean,show} ...

CLI Tool helps to show and clean artifacts in Artifactory,      can analyse the repository artifacts not downloaded for given number of weeks and delete them

positional arguments:
  {clean,show}  Specify clean or show as sub command
    clean       To clean artifactory artifacts not downloaded x no of weeks.
                Works Best for Docker based repos
    show        To Show Disk Memory details artifactory repositories given in
                sub command

optional arguments:
  -h, --help    show this help message and exit

Examples:
* Dry run for cleaning up artifacts not downloaded for x weeks. Default weeks to scan is 52w
cleanup_docker_artifacts.py clean --url $ARTIFACTORY_URL --repo $REPO_NAME --path sfrm -U $ARTIFACTORY_USER -P $API_KEY --before_weeks 30w
*  cleaning up cleaning up artifacts not downloaded for x weeks. Default weeks to scan is 52w
cleanup_docker_artifacts.py clean --url $ARTIFACTORY_URL --repo $REPO_NAME --path sfrm -U $ARTIFACTORY_USER -P $API_KEY --before_weeks 30w -d
* To show artifacts not downloaded for x weeks.  Default weeks to scan is 52w
cleanup_docker_artifacts.py show --url $ARTIFACTORY_URL --repo $REPO_NAME --path sfrm -U $ARTIFACTORY_USER -P $API_KEY --before_weeks 30w 
* Scan artifacts for Top Level REPO without REPO PATH. Default weeks to scan is 52w
cleanup_docker_artifacts.py show --url $ARTIFACTORY_URL --repo $REPO_NAME -U $ARTIFACTORY_USER -P $API_KEY --before_weeks 30w


===========================================================================================================================
*If you accidentally delete artifacts. You can restore them from Trash.  

````

