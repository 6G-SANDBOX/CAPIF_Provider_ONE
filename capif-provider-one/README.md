# Helm of capif-provider-one

![Version: 0.1.0](https://img.shields.io/badge/Version-0.1.0-informational?style=for-the-badge)
![Type: application](https://img.shields.io/badge/Type-application-informational?style=for-the-badge) 
![AppVersion: latest](https://img.shields.io/badge/AppVersion-latest-informational?style=for-the-badge) 

## Description

A Helm chart for capif-provider-one in Kubernetes

## Usage

## Values

| Key | Type | Default | Description |
|-----|------|---------|-------------|
| environment | string | `"openshift"` | The Environment variable. It accepts: 'kuberentes-athens', 'kuberentes-uma', 'openshift' |
| ingress_ip | object | `{"athens":"10.161.1.126","uma":"10.11.23.49"}` | If env: 'kuberentes-athens' or env: 'kuberentes-uma', use the Ip address dude for the kubernetes to your Ingress Controller ej: kubectl -n NAMESPACE_CAPIF get ing s |
| kubernetesClusterDomain | string | `"cluster.local"` |  |
| oneProviderGui.oneProviderGui.env.capifHostname | string | `"my-capif.apps.ocp-epg.hi.inet"` |  |
| oneProviderGui.oneProviderGui.env.capifPort | string | `"80"` |  |
| oneProviderGui.oneProviderGui.env.easyRsaPort | string | `"8083"` |  |
| oneProviderGui.oneProviderGui.env.requestsCaBundle | string | `"/usr/src/app/ca.crt"` |  |
| oneProviderGui.oneProviderGui.env.sslCertFile | string | `"/usr/src/app/ca.crt"` |  |
| oneProviderGui.oneProviderGui.image.repository | string | `"709233559969.dkr.ecr.eu-central-1.amazonaws.com/evolved5g:capif-one-provider-gui"` |  |
| oneProviderGui.oneProviderGui.image.tag | string | `""` |  |
| oneProviderGui.ports[0].name | string | `"capif-provider-one"` |  |
| oneProviderGui.ports[0].port | int | `8085` |  |
| oneProviderGui.ports[0].targetPort | int | `8085` |  |
| oneProviderGui.type | string | `"ClusterIP"` |  |






