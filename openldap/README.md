docker build -t openldap .

docker run \
--name openldap-container \
--env LDAP_ADMIN_PASSWORD="D1Wt#s5BAi7L" \
-p 389:389 \
-d openldap:latest
