# LDAP Load Testing

The purpose of this project is to load test the LDAP3 Python library. There are three services in this project:

1) OpenLDAP
1) Gateway Service
1) LDAP Service

The docker-compose.yml file loads property files from the top-level "configs" folder into the Gateway service and LDAP service containers.

# Starting the project

Run this command from the top-level folder.

```
docker-compose up
```

# Stoping the project
Run this command from the top-level folder.

```
docker-compose down
```

# Verifying the deployment

## OpenLDAP

When you run Docker Compose it builds a new OpenLDAP image and loads it with the LDIF file in the openldap directory. There are a copule of organizational units, groups, and users.

OpenLDAP is tested indirectly by the load tests when it is called by the LDAP Service. If you have Apache Directory Studio around, you can connect to OpenLDAP and verify that it is running:

* hostname - localhost
* port - 389
* bind dn - cn=admin,dc=byteworks,dc=com
* password - D1Wt#s5BAi7L (Extra points if you setup Docker compose to take the password as a command line argument. It will require a small coding change to the LDAP service too.)
* base dn - dc=byteworks,dc=com

## Gateway Service

Use the health check endpoint to verify that the Gateway Service is running.

 1) Go to the [Gateway Swagger UI page ](http://localhost:5000/api/docs/#/)
 2) Click on [GET /api/health_check](http://localhost:5000/api/docs/#/default/get_api_health_check)
 3) Click "Try it out"
 4) Click "Execute"

 You should see results like this:
```
 {
  "hostname": "6a33f775fab7",
  "ip_addr": "192.168.224.4",
  "status": "OK",
  "system": "src.gateway.api.gateway_api"
}
```

## LDAP Service

Use the health check endpoint to verify that the LDAP Service is running.

1) Stay on the [Gateway Swagger UI page ](http://localhost:5000/api/docs/#/)
2) Click on [GET /api​/ldap​/health_check](http://localhost:5000/api/docs/#/default/get_api_ldap_health_check)
3) Click "Try it out"
4) Click "Execute"

You should see results like this:
```
{
  "hostname": "9fa9dcfb8ffa",
  "ip_addr": "192.168.224.3",
  "status": "OK",
  "system": "src.ldap.api.ldap_api"
}
```

ALtenratively, go directly to the [LDAP Swagger UI page](http://localhost:5002/api/docs/#/default/get_api_health_check) and execute the LDAP healthcheck from there.


# Load Testing

Be sure that [JMeter](https://jmeter.apache.org/download_jmeter.cgi) is install and in your path.

## Start JMeter

```
jmeter
```

## Open the Load Test

The load tests are locate in the jmeter folder at the root of this project. There are two JMeter tests:

* CRUDTestJMeter.jmx - This thread group runs once and does an Add, Search, Modify, and Delete.
* APILoadTestJMeter.jmx - This thread group runs until it is manually stopped. It looks up the same user by UID over and over.
