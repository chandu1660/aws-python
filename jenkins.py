import jenkinsapi
from jenkinsapi.jenkins import Jenkins


server=Jenkins('http://localhost:8084', username='manikanta', password='@@5a3Gmk') 
print(server.keys())