# Dynamic Hosts Inventory

A tool for ansible that manages and lists a dynamic host inventory.

As DevOps engineers it is common that we have to perform administration and maintenance tasks on a large number of servers. These servers can be grouped by different categories, and the same tasks are not applied for all servers, but are specific tasks for each group of servers.

The purpose of this project is to manage a list of servers using JSON files as a database, and to generate a dynamic inventory that can be used by Ansible scripts.

## Usage

Clone this project

```bash
 git clone git@github.com:cppmx/dynamic_hosts.git
```

Now you can use the scripts [play.sh](#script-play) and [hosts.py](#script-hosts) to manage your list of servers and your Ansible scripts.

### Script hosts

You can register servers with the following data:

- Client: Each client will have their own data file, in this way you will be able to manage servers of different clients
- Environment: Refers to the development environment, can be any of the following values:
    - dev: If the server is in a development environment
    - itg: If the server is in an integration environment
    - pro: If the server is in a production environment
- Role: Refers to the role for which this server is used. It's possible values are:
    - app: If it is an application server
    - db: If it is a database server
    - web: If it is a web server
    - zoo: If it is a zookeeper server
- Location: This is a free field, here you can use any value to specify the location of your server, example: MEX for Mexico, IND for India, GER for Germany, etc.

The script recognizes the following parameters in the command line:

```bash
optional arguments:
  -h, --help            show this help message and exit
  --client CLIENT       A valid client
  --config              Display current configuration
  --env {dev,test,prod}
                        Execution environment of this script. By default it is
                        executed in production.
  --list                Returns all hosts that meet the criteria.
  --new-server          Add new server record.
  --test                Run tests
  --update-server       Update information of a server.
  --verbose, -v         Displays extra data in the console output. It should
                        not be used in production.
  --version             show program's version number and exit
```

* __IMPORTANT NOTE__: One thing is the server environment, and another the execution environment of this script. The env flag refers to the environment of the script, not the environment of the servers in the database.

So, how is this script used? Continue reading.

#### Show the configuration

Three possible scenarios or environments are considered to use this script:

- A testing environment: Normally used to run unit tests on this code.
    - The name of the client is *test_test*
    - The test database is stored in dynamic_hosts/db/test/test_prod/

- A development environment: This environment is useful for testing during the development of this code and its improvements.
    - The name of the client is *test_dev*
    - The test database is stored in dynamic_hosts/db/dev/test_dev/
 
 - A production environment: This environment is useful for testing during the development of this code and its improvements.
     - The name of the client is *test_prod*
     - The test database is stored in dynamic_hosts/db/dev/test_prod/

Below we can see how to view the current configuration that the script is using:

```bash
 $ ./hosts.py --config -v
 
 ***** D Y N A M I C   H O S T S *****
             CONFIGURATION
 *************************************
  - Client..............: test_prod
  - Environment.........: None
  - Role................: None
  - Location............: None
  - Database............: /home/user/dynamic_hosts/dynamic_hosts/db/prod/test_prod/data.json
  *************************************
```

From the previous example we can observe the following:

- It is a production environment, this can be deduced by the place where the database is stored:
    - /db/prod/client_name
- Since no name was specified for the client, then *test_prod* is used.
- No environment, role or location was specified for the servers, so if we requested the generation of an inventory for Ansible, it would return everything the database has at that moment.

If we want to change the environment we will use the ```--env``` parameter as follows:

```bash
 $ ./hosts.py --env dev --config -v
 
 ***** D Y N A M I C   H O S T S *****
             CONFIGURATION
 *************************************
  - Client..............: test_dev
  - Environment.........: None
  - Role................: None
  - Location............: None
  - Database............: /home/user/dynamic_hosts/dynamic_hosts/db/dev/test_dev/dev_data.json
  *************************************
```

If we want to use a different client name we will use the --client parameter:

```bash
 $ ./hosts.py --env dev --client MyClient --config -v
 
 ***** D Y N A M I C   H O S T S *****
             CONFIGURATION
 *************************************
  - Client..............: MyClient
  - Environment.........: None
  - Role................: None
  - Location............: None
  - Database............: /home/user/dynamic_hosts/dynamic_hosts/db/dev/MyClient/dev_data.json
  *************************************
```

The values for the environment, role and location fields are assigned by environment variables. The script looks for the following environment variables to assign these values:

- THE_CLIENT: If the script does not receive the name of the client as a parameter, then it will look for this environment variable. If this environment variable does not exist either, then it will use an arbitrary name by default.
- THE_ENVIRONMENT: The possible values for this environment variable are:
    - dev
    - itg
    - pro
- THE_ROLE: The possible values for this environment variable are:
    - app
    - db
    - web
    - zoo
- THE_LOCATION: It is expected that the value of this environment variable matches the values that you used in the database when registering your servers.

```bash
 $ THE_ENVIRONMENT=itg ./hosts.py --env dev --client MyClient --config -v
 
 ***** D Y N A M I C   H O S T S *****
             CONFIGURATION
 *************************************
  - Client..............: MyClient
  - Environment.........: itg
  - Role................: None
  - Location............: None
  - Database............: /home/user/dynamic_hosts/dynamic_hosts/db/dev/MyClient/dev_data.json
  *************************************
```

#### Add new server

Registering a new server is as simple as using the --new-server parameter as follows:

```bash
 $ ./hosts.py --new-server
 Please enter the following information:
  - Host................: demo.domain.net
  - Environment.........: itg
  - Role................: web
  - Location............: mex
 Do you want to add variables for this host (y/N)? y
 Variable name: shell
 Value for "shell" variable: bash
 Do you want to add another variable for this host (y/N)? n
```

If there are no errors in the data capture then the script will end normally returning a zero error code.

The possible errors that you can face are:
- Capture the same record twice. A duplicate registration is considered when the hostname is repeated, that is, there can not be two servers with the same hostname.
- Use an incorrect value for the environment or the role fields. In previous lines, the only possible values for these fields are specified.
- Create two variables for the host with the same name. This is obvious, there can not be two variables that are called the same for the same host.

To verify the server that you just registered, you can see the section on how to [obtain a dynamic inventory](#get-a-dynamic-inventory).

#### Update A Server Data

Update a server data is as simple as using the --update-server parameter as follows:

```bash
 $ ./hosts.py --update-server
 Please enter the following information:
  - Host................: demo.domain.net
  Current Host................: demo.domain.net
  Change it to..................:
  Current Environment.........: itg
  Change it to..................: dev
  Current Role................: web
  Change it to..................:
  Current Location............: mex
  Change it to..................: usa
 This host has variables
 Do you want to keep the current variables Y/n?
```

As we can see in the previous example, the first data requested is the name of the host. The script will search for this record and will show us one by one the current values and will ask us if we want to make any changes in them. If we only press enter then it will be considered that we do not want to make changes in that field.

If there are no errors in the data capture then the script will end normally returning a zero error code.

The possible errors that you can face are:
- Try changing the registry of a host that does not exist in the database.
- Capture the same record twice. A duplicate registration is considered when the hostname is repeated, that is, there can not be two servers with the same hostname.
- Use an incorrect value for the environment or the role fields. In previous lines, the only possible values for these fields are specified.
- Create two variables for the host with the same name. This is obvious, there can not be two variables that are called the same for the same host.

To verify the server that you just updated, you can see the section on how to [obtain a dynamic inventory](#get-a-dynamic-inventory).


#### Get A Dynamic Inventory

Ansible uses the --list parameter to obtain a dynamic inventory of a script. You can see that dynamic inventory also using this parameter as shown below:

```bash
 $ ./hosts.py --list
 {"_meta": {"hostvars": {}}, "all": {"hosts": [], "vars": {}}}
```

When there is no data in the database, or the database file has not yet been created, then it will return an empty inventory like the one shown in the previous example.

If there is already data in the database then we can see an output like the following:

```bash
 $ ./hosts.py --list
 {"_meta": {"hostvars": {"demo.domain.net": {"shell": "bash"}}}, "all": {"hosts": ["demo.domain.net"], "vars": {}}}
```

### Script play

This script uses a Docker container to run an Ansible playbook, the playbook will use the [hosts.py](#script-hosts) script to obtain the server inventory.

The script receives the following parameters:

```bash
$ ./play.sh --help
|--------------------------------------------------------------------------------|
|     A N S I B L E   W I T H   D Y N A M I C   H O S T S            |
|--------------------------------------------------------------------------------|
| Current environment ...                                                        |
|      Script Version ... 0.0.1                                                  |
|        Bash Version ... 4.4.19(2)-release                                      |
|         Description ... This script allows you to run a playbook in a container using a dynamic host list.|
|--------------------------------------------------------------------------------|

 Usage:
  play.sh CLIENT [ENVIRONMENT] [GROUP] [ROLES]

 Client:
        MyClient
 Environment:
   -e|--env        It sets the environment of the hosts.
                   If omitted, all environments will be used.
 The available environments are:
        all
        pro
        itg
        dev
 Groups:
   -g|--group       It sets the group of the hosts.
                    If omitted, a group called all will be used.
 The available groups are:
        all
        self
 Roles:
   -e|--env         It sets the role of the hosts.
                   If omitted, all roles will be used.
 The available roles are:
        all
        app
        db
        web
        zoo

 Expamples:
  play.sh MyClient
  It will execute the playbbok on all the hosts of the client . The hosts will be grouped into a group called all.
  {
      "all": {
          "hosts": [
              "hosta.domain.net",
              "hostb.domain.net"
          ],
          "vars": {}
      }
  }

  play.sh MyClient -e pro
  Execute playbbok on all hosts of client  that belong to environment pro. The hosts will be grouped into a group called all.
  {
      "all": {
          "hosts": [
              "hostc.domain.net",
              "hostd.domain.net"
          ],
          "vars": {}
      }
  }

  play.sh MyClient -g self
  It will execute the playbbok on all hosts of client  and they will be grouped in the group to which they belong.
  {
      "PRO": {
          "hosts": [
              "hosta.domain.net",
              "hostb.domain.net"
          ],
          "vars": {}
      }
      "DEV": {
          "hosts": [
              "hostc.domain.net",
              "hostd.domain.net"
          ],
          "vars": {}
      }
  }
```

Before deploying this help the script will verify that there is already at least one client captured in the production environment. If you do not find any client for production then the script will show an error message like the following:

```bash
$ ./play.sh --help
[ERROR] No client has yet been defined
[ERROR] Please first capture some servers for some client
[ERROR] Test clients are not valid
[ERROR] To add a server use one of the following commands:
[ERROR]   hosts.py --client <CLIENT_NAME> --new-server
[ERROR]   python3 hosts.py --client <CLIENT_NAME> --new-server
```

Once you have captured at least one server for a client in the production database, this script will allow you to continue with the execution of the playbook.

By default, the playbook will ping the list of servers that generate the dynamic inventory.

This works in the following way, suppose we have captured the following servers:

| Host | Client | Environment | Role | Location |
| --- | --- | --- | --- | --- |
| app1.client1.domain.net | Client1 | pro | app | usa |
| app2.client1.domain.net | Client1 | itg | app | mex |
| db1.client1.domain.net | Client1 | pro | db | usa |
| db2.client1.domain.net | Client1 | dev | db | ind |
| web1.client1.domain.net | Client1 | pro | web | ger |
| web2.client1.domain.net | Client1 | pro | web | fra |
| zoo1.client1.domain.net | Client1 | pro | zoo | usa |
| zoo2.client1.domain.net | Client1 | itg | zoo | arg |
| app1.client2.domain.net | Client2 | pro | app | usa |
| app2.client2.domain.net | Client2 | pro | app | mex |
| db1.client2.domain.net | Client2 | pro | db | usa |
| db2.client2.domain.net | Client2 | pro | db | ind |
| web1.client2.domain.net | Client2 | pro | web | ger |
| web2.client2.domain.net | Client2 | pro | web | fra |
| zoo1.client2.domain.net | Client2 | pro | zoo | usa |
| zoo2.client2.domain.net | Client2 | pro | zoo | arg |

Now, with the above information, suppose we want to ping all the web servers of client 2, then we will do the following:

```bash
$ ./play.sh Client2 --role web
```

To run the playbook on all servers that are in use we do the following:

```bash
$ ./play.sh Client2 --location web
```

If we want to do the same thing now, but with the servers of client 1 that are in an ITG environment, we do the following:

```bash
$ ./play.sh Client1 --env itg
```

Obviously you can combine these parameters and make the filter that suits your needs.

# TODO
This script was created and tested in a secure environment where folder sharing is not allowed, for this reason it is necessary to use a volume for the container and make changes dynamically.

Currently if you want to make changes in the BD and then execute your scripts it is necessary to recreate the image.

