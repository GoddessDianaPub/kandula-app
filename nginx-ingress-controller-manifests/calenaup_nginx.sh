kubectl delete clusterrole ingress-nginx
kubectl delete clusterrolebinding ingress-nginx
kubectl delete ValidatingWebhookConfiguration ingress-nginx-admission
kubectl delete ns ingress-nginx
sleep 5