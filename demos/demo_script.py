from argo_metadata_validator.validation import ArgoValidator
from pprint import pprint

validation_results = ArgoValidator().validate(["files/valid_sensor.json", "files/invalid_sensor.json"])

pprint(validation_results)
