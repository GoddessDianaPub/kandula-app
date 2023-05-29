kubectl apply -f kandula-configmap.yaml
kubectl apply -f kandula-sa.yaml
#kubectl create token kandula-sa
kubectl apply -f kandula-role-read.yaml
kubectl apply -f kandula-role-read-bind.yaml
kubectl apply -f kandula-role-edit.yaml
kubectl apply -f kandula-role-edit-bind.yaml
kubectl apply -f kandula_deploy.yaml
kubectl apply -f kandula-service-lb.yaml


sleep 10