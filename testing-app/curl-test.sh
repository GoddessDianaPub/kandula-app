for i in {1..20}; do
   kubectl exec --namespace=kandula curl -- sh -c 'test=`wget -qO- -T 2  http://webapp-service.default.svc.cluster>
   echo ""
done