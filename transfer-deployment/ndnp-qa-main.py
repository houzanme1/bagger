#!/usr/bin/env python
""" Deploys a build of the NDNP Transfer project to QA 
"""

from transfer.core import workflow, broker, package as core_package
from transfer.projects.ndnp import webapp, package as ndnp_package

config = {
    'DEBUG': False, # If True, will print out actions rather than take them (e.g., will not hit database)
    'PSQL': '/usr/bin/psql', # Tell me where to find psql (default = '/usr/bin/psql')
    'PGHOST': 'localhost', # This is the host that the PostgreSQL database lives on (default = localhost)
    'PGPORT': '5433', # This is the port that PostgreSQL listens on (default = 5432)
    'PGUSER': 'postgres', # This is a username on PostgreSQL with SUPERUSER privlidges (default = postgres)
    'PGPASSWORD': '', # This is the password for the user specified above (default = '')
    'CATALINA_HOME': "", # Tell me where to find Tomcat (default = '/opt/coolstack/tomcat')    
    'DB_PREFIX': 'qa', # This will prepend a custom prefix to the database name that will get created.  An _ will be appended. (default = '')
    'ROLE_PREFIX': 'qa', # This will prepend a custom prefix to the roles that will get created.  An _ will be appended. (default = '')
    'INSTALL_DIR': 'install', # Set the directory that the CLI tools will be unzipped to (default = '.')
    'VERSION': '1.5', # This is the version of the release being deployed
    'SQL_FILES_LOCATION': '/home/mjg/workspace/transport-perl/db', #Set the location of the sql files (default = '')
    'TRANSFER_PASSWD': '', # Set a password for the package modeler user role (default = 'transfer_user')
    'JBPM_PASSWD': '', # Set a password for the jbpm role (default = 'jbpm_user')
    'REQUEST_BROKER_PASSWD': '', # Set a password for the service_request_broker role (default = 'service_request_broker_user')            
    'TOMCAT_START': '', # Set the invocation of starting tomcat (default = '/usr/sbin/svcadm disable svc:/application/csk-tomcat')
    'TOMCAT_STOP': '', # Set the invocation of stopping tomcat (default = '/usr/sbin/svcadm enable svc:/application/csk-tomcat')
}

jbpm = workflow.Jbpm(config)
core_modeler = core_package.PackageModeler(config)
ndnp_modeler = ndnp_package.PackageModeler(config)
request_broker = broker.RequestBroker(config)
ndnp_webapp = webapp.WebApp(config)

# Uncomment to drop dbs and roles
print jbpm.drop()
print core_modeler.drop()
print request_broker.drop()

# Uncomment to create dbs, roles, load with fixtures
print jbpm.create_database()
print core_modeler.create_database()
print request_broker.create_database()

print jbpm.create_roles()
print core_modeler.create_roles()
print request_broker.create_roles()

print jbpm.create_tables()
print core_modeler.create_tables()
print ndnp_modeler.create_tables()
print request_broker.create_tables()

print jbpm.grant_permissions()
print core_modeler.grant_permissions()
print ndnp_modeler.grant_permissions()
print request_broker.grant_permissions()

print jbpm.deploy_drivers()
print core_modeler.deploy_drivers()
print ndnp_modeler.deploy_drivers()

print jbpm.create_fixtures(fixtures="jbpm-ndnp-qa-fixtures.sql")
print core_modeler.create_fixtures(fixtures=(
        'createrepository -id ndnp',
        'createperson -id ray -firstname Ray -surname Murray',
        'createperson -id myron -firstname Myron -surname Briggs',
        'createperson -id scott -firstname Scott -surname Phelps',
        'createperson -id brian -firstname Brian -surname Vargas',
        'createperson -id jjoyner-qr -firstname JoKeeta -surname Joyner',
        'createperson -id jjoyner-sysadmin -firstname JoKeeta -surname Joyner',
        'createperson -id jjoyner-ingest -firstname JoKeeta -surname Joyner',
        'createperson -id tami-qr -firstname Tasmin -surname Mills',
        'createperson -id tami-sysadmin -firstname Tasmin -surname Mills',
        'createperson -id tami-ingest -firstname Tasmin -surname Mills',
        'createperson -id lfre-qr -firstname LaTonya -surname Freeman',
        'createperson -id lfre-sysadmin -firstname LaTonya -surname Freeman',
        'createperson -id lfre-ingest -firstname LaTonya -surname Freeman',
        'createsystem -id rdc-workflow',
        'createsystem -id transfer-components-core-%s' % config['VERSION'],
        'createrole -id repository_system',
        'createsystem -id ndnp-staging-repository -roles repository_system',
        'createrole -id storage_system',
        'createsystem -id rdc -roles storage_system',
        'createsystem -id rs15 -roles storage_system',
        'createsystem -id rs25 -roles storage_system',
        'createrole -id ndnp_awardee',
        'createorganization -id CU-Riv -name "CA - University of California, Riverside" -roles ndnp_awardee',
        'createorganization -id FUG -name "FL - University of Florida Libraries, Gainesville" -roles ndnp_awardee',
        'createorganization -id KyU -name "KY - University of Kentucky Libraries, Lexington" -roles ndnp_awardee',
        'createorganization -id NN -name "NY - New York Public Library, New York City" -roles ndnp_awardee',
        'createorganization -id UUML -name "UT - University of Utah, Salt Lake City" -roles ndnp_awardee',
        'createorganization -id VIC -name "VA - Library of Virginia, Richmond" -roles ndnp_awardee',
        'createorganization -id DLC -name "LC - Library of Congress" -roles ndnp_awardee',
        'createorganization -id MnHi -name "MN - Minnesota Historical Society" -roles ndnp_awardee',
        'createorganization -id NbU -name "NE - University of Nebraska, Lincoln" -roles ndnp_awardee',
        'createorganization -id TxDN -name "TX - University of North Texas, Denton" -roles ndnp_awardee',
       ))
print ndnp_modeler.create_fixtures(fixtures=(
        'createawardphase -name "2005"',
        'createawardphase -name "2006"',
        'createawardphase -name "2007"',
        'createawardphase -name "2008"',
       ))

print ndnp_modeler.deploy_process_def(jbpm.driver)
print ndnp_webapp.deploy()
