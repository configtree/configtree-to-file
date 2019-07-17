# Usage
Running this docker image, it will create a configuration file in the local filesystem
```
docker run \
-v /path/to/save/config:/config_file \
--env EMAIL=YOUR_CONFIGTREE_EMAIL \
--env ORGSLUG=ORGANIZATION_SLUG \
--env PASSWORD=YOUR_PASSWORD \
configtree-to-file -a Application_Name -e Environment_Name -v Version_name -f config_file_name
```
## Supported config extension
`.properties`

More are coming