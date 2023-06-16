#Create kandula deployment
kubectl apply -f kandula_deploy.yaml

sleep 60

#Create kandula service
kubectl apply -f kandula-service.yaml

kubectl get nodes -o wide
