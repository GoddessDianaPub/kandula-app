kubectl delete deploy kandula-app
kubectl delete svc kandula-service
kubectl delete role pod-reader
kubectl delete rolebinding pod-reader-binding
kubectl delete role pod-editor
kubectl delete rolebinding pod-editor-binding
kubens default
kubectl delete ns kandula

sleep 10

#terraform state rm module.eks.kubernetes_namespace.kandula_ns
#terraform state rm module.eks.kubernetes_service_account.opsschool_sa

