from typing import List, Optional, Dict, Any
from pydantic import BaseModel

class IpSecurityRestriction(BaseModel):
    action: str
    description: str
    ipAddressRange: str
    name: str

class Traffic(BaseModel):
    latestRevision: bool
    weight: int

class StickySessions(BaseModel):
    affinity: str

class Ingress(BaseModel):
    allowInsecure: bool
    clientCertificateMode: str
    corsPolicy: Optional[Any]
    customDomains: Optional[Any]
    external: bool
    ipSecurityRestrictions: List[IpSecurityRestriction]
    stickySessions: StickySessions
    targetPort: int
    traffic: List[Traffic]
    transport: str

class Registry(BaseModel):
    identity: str
    passwordSecretRef: str
    server: str
    username: str

class Secret(BaseModel):
    name: str
    value: Optional[str] = None

class EnvVar(BaseModel):
    name: str
    value: str

class Resources(BaseModel):
    cpu: float
    ephemeralStorage: str
    memory: str

class Container(BaseModel):
    env: Optional[List[EnvVar]] = []
    image: str
    name: str
    probes: Optional[List[Any]] = []  # Could be more specific if probe structure is known
    resources: Resources

class Scale(BaseModel):
    cooldownPeriod: int
    maxReplicas: int
    minReplicas: int
    pollingInterval: int
    rules: Optional[Any]

class Template(BaseModel):
    containers: List[Container]
    initContainers: Optional[Any]
    scale: Scale
    serviceBinds: Optional[Any]
    terminationGracePeriodSeconds: Optional[int]
    volumes: Optional[List[Any]] = []  # Could be more specific if volume structure is known

class Configuration(BaseModel):
    activeRevisionsMode: str
    dapr: Optional[Any]
    identitySettings: List[Any]
    ingress: Ingress
    registries: Optional[List[Registry]] = []
    runtime: Optional[Any]
    secrets: Optional[List[Secret]] = []
    service: Optional[Any]

class Properties(BaseModel):
    configuration: Configuration
    template: Template
    workloadProfileName: str

class ContainerApp(BaseModel):
    name: str
    properties: Properties
    environmentId: Optional[str] = None
    resourceGroup: str
    type: str

class ContainerAppEntry(BaseModel):
    filename: str
    is_dirty: bool

class Partitura(BaseModel):
    resource_group: str
    apps: Dict[str, ContainerAppEntry]