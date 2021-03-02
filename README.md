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

## OPENLDAP

WHen you run Docker compose it builds a new OpenLDAP image and loads it with LDIF file in the openldap directory. It has a copule of organizational units and two users.

OpenLDAP is tested indirectly when you run the load tests and it is called by the LDAP Service. If you have Apache Directory Studio around you can connect to OpenLDAP and verify that it is running:

* hostname - localhost
* port - 389
* bind dn - cn=admin,dc=byteworks,dc=com
* password - D1Wt#s5BAi7L (Extra points if you setup Docker compose to take the password as a command line argument. It will require a small coding change to the LDAP service too.)
* base dn - dc=byteworks,dc=com

## GATEWEAY

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

## LDAP SERVICE

1) Go to the [Gateway Swagger UI page ](http://localhost:5000/api/docs/#/)
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


# LOAD TESTING

Be sure that JMeter is install and in your path.

## Start JMeter

```
jmeter
```

## Open the Load Test

The load tests are in the root of this project inside the jmeter folder:

* CRUDTestJMeter.jmx - This thread group runs once and does an Add, Search, Modify, and Delete.
* APILoadTestJMeter.jmx - This thread group runs until it is manually stopped. It looks up the same user by UID over and over.
