# API
1) non - malicious - curl -H "Content-Type:application/json" -X POST -d "{\"user\":0,\"role\":0,\"query\":\"10,21,12\"}" http://192.168.43.50:5000/checker
2) malicious - curl -H "Content-Type:application/json" -X POST -d "{\"user\":2,\"role\":0,\"query\":\"12,25,13,02,25,40,01,10,46\"}" http://192.168.43.50:5000/checker